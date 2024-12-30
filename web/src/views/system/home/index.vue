<template>
	<div class="home-container">
		<el-row :gutter="15" class="home-card-one mb15">
			<el-col
				:xs="24"
				:sm="12"
				:md="12"
				:lg="6"
				:xl="6"
				v-for="(v, k) in homeOne"
				:key="k"
				:class="{ 'home-media home-media-lg': k > 1, 'home-media-sm': k === 1 }"
			>
				<div class="home-card-item flex cyber-card">
					<div class="flex-margin flex w100" :class="` home-one-animation${k}`">
						<div class="flex-auto">
							<span class="font30 cyber-text">{{ v.num1 }}</span>
							<span class="ml5 font16" :style="{ color: v.color1 }">{{ v.num2 }}</span>
							<div class="mt10 cyber-label">{{ v.num3 }}</div>
						</div>
						<div class="home-card-item-icon flex cyber-icon" :style="{ background: `var(${v.color2})` }">
							<i class="flex-margin font32" :class="v.num4" :style="{ color: `var(${v.color3})` }"></i>
						</div>
					</div>
				</div>
			</el-col>
		</el-row>
		<el-row :gutter="15" class="home-card-two mb15">
			<el-col :xs="24" :sm="14" :md="14" :lg="16" :xl="16">
				<div class="home-card-item cyber-card">
					<div style="height: 100%" ref="homeLineRef" class="chart-container"></div>
				</div>
			</el-col>
			<el-col :xs="24" :sm="10" :md="10" :lg="8" :xl="8" class="home-media">
				<div class="home-card-item cyber-card">
					<div style="height: 100%" ref="homePieRef" class="chart-container"></div>
				</div>
			</el-col>
		</el-row>
		<el-row :gutter="15" class="home-card-three">
			<el-col :xs="24" :sm="10" :md="10" :lg="8" :xl="8">
				<div class="home-card-item cyber-card">
					<div class="home-card-item-title cyber-title">列车实时监控指标</div>
					<div class="home-monitor">
						<div class="flex-warp">
							<div class="flex-warp-item" v-for="(v, k) in homeThree" :key="k">
								<div class="flex-warp-item-box cyber-monitor-item" :class="`home-animation${k}`">
									<div class="flex-margin">
										<i :class="v.icon" :style="{ color: v.iconColor }"></i>
										<span class="pl5 cyber-label">{{ v.label }}</span>
										<div class="mt10 cyber-value">{{ v.value }}</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</el-col>
			<el-col :xs="24" :sm="14" :md="14" :lg="16" :xl="16" class="home-media">
				<div class="home-card-item cyber-card">
					<div style="height: 100%" ref="homeBarRef" class="chart-container"></div>
				</div>
			</el-col>
		</el-row>
	</div>
</template>

<script lang="ts">
import { toRefs, reactive, defineComponent, onMounted, ref, watch, nextTick, onActivated, onBeforeUnmount } from 'vue';
import * as echarts from 'echarts';
import { storeToRefs } from 'pinia';
import { useThemeConfig } from '/@/stores/themeConfig';
import { useTagsViewRoutes } from '/@/stores/tagsViewRoutes';
import mittBus from '/@/utils/mitt';
import systemDataWebsocket from '/@/utils/systemDataWebsocket';

let global: any = {
	homeChartOne: null,
	homeChartTwo: null,
	homeCharThree: null,
	dispose: [null, '', undefined],
};

export default defineComponent({
	name: 'home',
	setup() {
		const homeLineRef = ref();
		const homePieRef = ref();
		const homeBarRef = ref();
		const storesTagsViewRoutes = useTagsViewRoutes();
		const storesThemeConfig = useThemeConfig();
		const { themeConfig } = storeToRefs(storesThemeConfig);
		const { isTagsViewCurrenFull } = storeToRefs(storesTagsViewRoutes);
		const state = reactive({
			homeOne: [
				{
					num1: '0',
					num2: '0',
					num3: '列车速度(km/h)',
					num4: 'fa fa-train',
					color1: '#FF6462',
					color2: '--next-color-primary-lighter',
					color3: '--el-color-primary',
				},
				{
					num1: '0',
					num2: '0',
					num3: '电机温度(℃)',
					num4: 'fa fa-thermometer',
					color1: '#6690F9',
					color2: '--next-color-success-lighter',
					color3: '--el-color-success',
				},
				{
					num1: '0',
					num2: '0',
					num3: '轴承振动(mm/s)',
					num4: 'fa fa-exclamation-triangle',
					color1: '#6690F9',
					color2: '--next-color-warning-lighter',
					color3: '--el-color-warning',
				},
				{
					num1: '0',
					num2: '0',
					num3: '制动压力(MPa)',
					num4: 'fa fa-tachometer',
					color1: '#FF6462',
					color2: '--next-color-danger-lighter',
					color3: '--el-color-danger',
				},
			],
			homeThree: [
				{
					icon: 'fa fa-battery-full',
					label: '蓄电池电压',
					value: '0V',
					iconColor: '#F72B3F',
				},
				{
					icon: 'fa fa-bolt',
					label: '牵引电流',
					value: '0A',
					iconColor: '#91BFF8',
				},
				{
					icon: 'fa fa-thermometer-half',
					label: '轮轴温度',
					value: '0℃',
					iconColor: '#88D565',
				},
				{
					icon: 'fa fa-tachometer',
					label: '空气压力',
					value: '0MPa',
					iconColor: '#88D565',
				},
				{
					icon: 'fa fa-volume-up',
					label: '噪声水平',
					value: '0dB',
					iconColor: '#FBD4A0',
				},
				{
					icon: 'fa fa-dashboard',
					label: '齿轮箱温度',
					value: '0℃',
					iconColor: '#FBD4A0',
				},
			],
			myCharts: [] as echarts.ECharts[],
			charts: {
				theme: '',
				bgColor: '',
				color: '#303133',
			},
		});
		const timeData: string[] = [];
		// 更新图表数据
		const updateCharts = (data: any) => {
			// 更新顶部卡片数据
			state.homeOne[0].num1 = data.speed || '0';
			state.homeOne[1].num1 = data.motorTemp || '0';
			state.homeOne[2].num1 = data.bearingVib || '0';
			state.homeOne[3].num1 = data.brakePressure || '0';

			// 更新监控指标数据
			state.homeThree[0].value = `${data.batteryVoltage || '0'}V`;
			state.homeThree[1].value = `${data.tractionCurrent || '0'}A`;
			state.homeThree[2].value = `${data.wheelTemp || '0'}℃`;
			state.homeThree[3].value = `${data.airPressure || '0'}MPa`;
			state.homeThree[4].value = `${data.noiseLevel || '0'}dB`;
			state.homeThree[5].value = `${data.gearboxTemp || '0'}℃`;

			// 使用后端的 timestamp 作为当前时间
			const backendTimestamp = data.timestamp || new Date().toLocaleTimeString();

			// 解析时间（可选，只取时间部分）
			const parsedTime = backendTimestamp.split(' ')[1] || backendTimestamp;

			// 更新时间数据
			timeData.push(parsedTime);
			if (timeData.length > 30) {
				timeData.shift();
			}

			// 更新折线图
			if (global.homeChartOne) {
				const option = global.homeChartOne.getOption();

				// 更新x轴数据
				option.xAxis[0].data = timeData;
				// 添加新的数据点
				option.series[0].data.push(data.speed);
				option.series[1].data.push(data.motorTemp);
				// 保持最近 30 个数据点
				if (option.series[0].data.length > 30) {
					option.series[0].data.shift();
					option.series[1].data.shift();
				}
				option.series[0].animation = false;
				option.series[0].showSymbol = false;
				option.series[1].animation = false;
				option.series[1].showSymbol = false;
				global.homeChartOne.setOption(option);
			}

			// 更新饼图
			if (global.homeChartTwo) {
				const option = global.homeChartTwo.getOption();
				option.series[0].data = [
					{ name: '正常运行', value: data.normalCount || 0 },
					{ name: '轻微故障', value: data.minorFaultCount || 0 },
					{ name: '严重故障', value: data.severeFaultCount || 0 },
				];
				global.homeChartTwo.setOption(option);
			}

			// 更新柱状图
			if (global.homeCharThree) {
				const option = global.homeCharThree.getOption();
				if (data.chartData) {
					option.series[0].data = data.chartData.vibrationData || [];
					option.series[1].data = data.chartData.temperatureData || [];
					global.homeCharThree.setOption(option);
				}
			}
		};

		// 折线图
		const initLineChart = () => {
			if (!global.dispose.some((b: any) => b === global.homeChartOne)) global.homeChartOne.dispose();
			global.homeChartOne = echarts.init(homeLineRef.value, state.charts.theme);
			const option = {
				backgroundColor: 'transparent',
				title: {
					text: '列车运行趋势',
					x: 'left',
					textStyle: { 
						fontSize: '15',
						color: '#00f3ff',
						fontWeight: 'bold',
						textShadow: '0 0 10px rgba(0,243,255,0.5)'
					},
				},
				grid: { 
					top: 70,
					right: 20,
					bottom: 30,
					left: 30,
					borderColor: 'rgba(0,243,255,0.1)'
				},
				tooltip: { 
					trigger: 'axis',
					backgroundColor: 'rgba(16,20,31,0.9)',
					borderColor: '#00f3ff',
					textStyle: {
						color: '#fff'
					}
				},
				legend: { 
					data: ['速度', '温度'],
					right: 0,
					textStyle: {
						color: '#fff'
					}
				},
				xAxis: {
					type: 'category',
					data: timeData,
					boundaryGap: false,
					axisLine: {
						lineStyle: {
							color: 'rgba(0,243,255,0.3)'
						}
					},
					axisLabel: {
						color: '#fff'
					}
				},
				yAxis: [
					{
						type: 'value',
						name: '数值',
						splitLine: { 
							show: true,
							lineStyle: {
								type: 'dashed',
								color: 'rgba(0,243,255,0.1)'
							}
						},
						axisLine: {
							lineStyle: {
								color: 'rgba(0,243,255,0.3)'
							}
						},
						axisLabel: {
							color: '#fff'
						}
					},
				],
				series: [
					{
						name: '速度',
						type: 'line',
						smooth: true,
						symbol: 'none',
						lineStyle: {
							width: 3,
							color: {
								type: 'linear',
								x: 0,
								y: 0,
								x2: 0,
								y2: 1,
								colorStops: [{
									offset: 0, color: '#00f3ff'
								}, {
									offset: 1, color: '#0051ff'
								}]
							},
							shadowColor: 'rgba(0,243,255,0.5)',
							shadowBlur: 10
						},
						areaStyle: {
							opacity: 0.2,
							color: {
								type: 'linear',
								x: 0,
								y: 0,
								x2: 0,
								y2: 1,
								colorStops: [{
									offset: 0, color: 'rgba(0,243,255,0.3)'
								}, {
									offset: 1, color: 'rgba(0,81,255,0.1)'
								}]
							}
						},
						data: [],
					},
					{
						name: '温度',
						type: 'line',
						smooth: true,
						symbol: 'none',
						lineStyle: {
							width: 3,
							color: {
								type: 'linear',
								x: 0,
								y: 0,
								x2: 0,
								y2: 1,
								colorStops: [{
									offset: 0, color: '#ff00f7'
								}, {
									offset: 1, color: '#ff5c00'
								}]
							},
							shadowColor: 'rgba(255,0,247,0.5)',
							shadowBlur: 10
						},
						areaStyle: {
							opacity: 0.2,
							color: {
								type: 'linear',
								x: 0,
								y: 0,
								x2: 0,
								y2: 1,
								colorStops: [{
									offset: 0, color: 'rgba(255,0,247,0.3)'
								}, {
									offset: 1, color: 'rgba(255,92,0,0.1)'
								}]
							}
						},
						data: [],
					},
				],
			};
			global.homeChartOne.setOption(option);
			state.myCharts.push(global.homeChartOne);
		};

		// 饼图
		const initPieChart = () => {
			if (!global.dispose.some((b: any) => b === global.homeChartTwo)) global.homeChartTwo.dispose();
			global.homeChartTwo = echarts.init(homePieRef.value, state.charts.theme);
			const option = {
				backgroundColor: 'transparent',
				title: {
					text: '列车状态分布',
					x: 'left',
					textStyle: { 
						fontSize: '15',
						color: '#00f3ff',
						fontWeight: 'bold',
						textShadow: '0 0 10px rgba(0,243,255,0.5)'
					},
				},
				tooltip: {
					trigger: 'item',
					backgroundColor: 'rgba(16,20,31,0.9)',
					borderColor: '#00f3ff',
					textStyle: {
						color: '#fff'
					}
				},
				legend: {
					orient: 'vertical',
					right: '0%',
					top: 'center',
					textStyle: {
						color: '#fff'
					}
				},
				series: [
					{
						type: 'pie',
						radius: ['50%', '70%'],
						center: ['40%', '50%'],
						itemStyle: {
							borderColor: '#000',
							borderWidth: 2
						},
						label: {
							show: false
						},
						emphasis: {
							label: {
								show: true,
								color: '#fff',
								formatter: '{b}: {d}%'
							},
							itemStyle: {
								shadowBlur: 10,
								shadowOffsetX: 0,
								shadowColor: 'rgba(0,243,255,0.5)'
							}
						},
						data: [
							{
								name: '正常运行',
								value: 0,
								itemStyle: {
									color: {
										type: 'linear',
										x: 0,
										y: 0,
										x2: 1,
										y2: 1,
										colorStops: [{
											offset: 0, color: '#00f3ff'
										}, {
											offset: 1, color: '#0051ff'
										}]
									}
								}
							},
							{
								name: '轻微故障',
								value: 0,
								itemStyle: {
									color: {
										type: 'linear',
										x: 0,
										y: 0,
										x2: 1,
										y2: 1,
										colorStops: [{
											offset: 0, color: '#ff00f7'
										}, {
											offset: 1, color: '#ff5c00'
										}]
									}
								}
							},
							{
								name: '严重故障',
								value: 0,
								itemStyle: {
									color: {
										type: 'linear',
										x: 0,
										y: 0,
										x2: 1,
										y2: 1,
										colorStops: [{
											offset: 0, color: '#ff0000'
										}, {
											offset: 1, color: '#ff5c00'
										}]
									}
								}
							}
						],
					},
				],
			};
			global.homeChartTwo.setOption(option);
			state.myCharts.push(global.homeChartTwo);
		};

		// 柱状图
		const initBarChart = () => {
			if (!global.dispose.some((b: any) => b === global.homeCharThree)) global.homeCharThree.dispose();
			global.homeCharThree = echarts.init(homeBarRef.value, state.charts.theme);
			const option = {
				backgroundColor: 'transparent',
				title: {
					text: '振动与温度分析',
					x: 'left',
					textStyle: { 
						fontSize: '15',
						color: '#00f3ff',
						fontWeight: 'bold',
						textShadow: '0 0 10px rgba(0,243,255,0.5)'
					},
				},
				tooltip: {
					trigger: 'axis',
					backgroundColor: 'rgba(16,20,31,0.9)',
					borderColor: '#00f3ff',
					textStyle: {
						color: '#fff'
					}
				},
				legend: {
					data: ['振动值', '温度值'],
					right: 0,
					textStyle: {
						color: '#fff'
					}
				},
				grid: {
					top: 70,
					right: 20,
					bottom: 30,
					left: 30,
					borderColor: 'rgba(0,243,255,0.1)'
				},
				xAxis: {
					type: 'category',
					data: ['轴承1', '轴承2', '轴承3', '轴承4', '电机', '齿轮箱'],
					axisLine: {
						lineStyle: {
							color: 'rgba(0,243,255,0.3)'
						}
					},
					axisLabel: {
						color: '#fff'
					}
				},
				yAxis: [
					{
						type: 'value',
						name: '数值',
						splitLine: {
							show: true,
							lineStyle: {
								type: 'dashed',
								color: 'rgba(0,243,255,0.1)'
							}
						},
						axisLine: {
							lineStyle: {
								color: 'rgba(0,243,255,0.3)'
							}
						},
						axisLabel: {
							color: '#fff'
						}
					},
				],
				series: [
					{
						name: '振动值',
						type: 'bar',
						barWidth: 15,
						itemStyle: {
							color: {
								type: 'linear',
								x: 0,
								y: 0,
								x2: 0,
								y2: 1,
								colorStops: [{
									offset: 0, color: '#00f3ff'
								}, {
									offset: 1, color: '#0051ff'
								}]
							},
							borderRadius: [4, 4, 0, 0]
						},
						data: [],
					},
					{
						name: '温度值',
						type: 'bar',
						barWidth: 15,
						itemStyle: {
							color: {
								type: 'linear',
								x: 0,
								y: 0,
								x2: 0,
								y2: 1,
								colorStops: [{
									offset: 0, color: '#ff00f7'
								}, {
									offset: 1, color: '#ff5c00'
								}]
							},
							borderRadius: [4, 4, 0, 0]
						},
						data: [],
					},
				],
			};
			global.homeCharThree.setOption(option);
			state.myCharts.push(global.homeCharThree);
		};

		// 批量设置 echarts resize
		const initEchartsResizeFun = () => {
			nextTick(() => {
				for (let i = 0; i < state.myCharts.length; i++) {
					setTimeout(() => {
						state.myCharts[i].resize();
					}, i * 1000);
				}
			});
		};

		// 批量设置 echarts resize
		const initEchartsResize = () => {
			window.addEventListener('resize', initEchartsResizeFun);
		};

		// 页面加载时
		onMounted(() => {
			initEchartsResize();
			// 初始化所有图表
			initLineChart();
			initPieChart();
			initBarChart();
			// 启动 WebSocket
			systemDataWebsocket.init();
			mittBus.on('homeWebsocket', (data: any) => {
				updateCharts(data);
			});
		});

		// 页面卸载时
		onBeforeUnmount(() => {
			window.removeEventListener('resize', initEchartsResizeFun);
			mittBus.off('homeWebsocket');
			systemDataWebsocket.close();
		});

		// 由于页面缓存原因，keep-alive
		onActivated(() => {
			initEchartsResizeFun();
		});

		// 监听 vuex 中的 tagsview 开启全屏变化
		watch(
			() => isTagsViewCurrenFull.value,
			() => {
				initEchartsResizeFun();
			}
		);

		// 监听深色主题
		watch(
			() => themeConfig.value.isIsDark,
			(isIsDark) => {
				nextTick(() => {
					state.charts.theme = isIsDark ? 'dark' : '';
					state.charts.bgColor = isIsDark ? 'transparent' : '';
					state.charts.color = isIsDark ? '#dadada' : '#303133';
					// 重新初始化所有图表
					initLineChart();
					initPieChart();
					initBarChart();
				});
			},
			{
				deep: true,
				immediate: true,
			}
		);

		return {
			homeLineRef,
			homePieRef,
			homeBarRef,
			...toRefs(state),
		};
	},
});
</script>

<style scoped lang="scss">
$homeNavLengh: 8;
$cyber-primary: #00f3ff;
$cyber-secondary: #0051ff;
$cyber-accent: #ff00f7;
$cyber-bg: rgba(16, 20, 31, 0.8);

.home-container {
	overflow: hidden;
	background: linear-gradient(135deg, #0a0e17 0%, #1a1f2c 100%);
	padding: 20px;
	min-height: 100vh;

	.cyber-card {
		background: $cyber-bg !important;
		border: 1px solid rgba($cyber-primary, 0.3) !important;
		box-shadow: 0 0 15px rgba($cyber-primary, 0.1) !important;
		backdrop-filter: blur(10px);
		position: relative;
		overflow: hidden;

		&::before {
			content: '';
			position: absolute;
			top: 0;
			left: 0;
			right: 0;
			height: 1px;
			background: linear-gradient(90deg, transparent, $cyber-primary, transparent);
			animation: cyber-scan 2s linear infinite;
		}
	}

	.cyber-text {
		color: $cyber-primary;
		text-shadow: 0 0 10px rgba($cyber-primary, 0.5);
	}

	.cyber-label {
		color: rgba(255, 255, 255, 0.7);
		font-size: 0.9em;
	}

	.cyber-value {
		color: $cyber-primary;
		font-size: 1.2em;
		font-weight: bold;
	}

	.cyber-title {
		color: $cyber-primary;
		font-size: 1.2em;
		font-weight: bold;
		text-transform: uppercase;
		letter-spacing: 1px;
		margin-bottom: 20px;
		text-shadow: 0 0 10px rgba($cyber-primary, 0.5);
	}

	.cyber-icon {
		background: rgba($cyber-secondary, 0.2) !important;
		border: 1px solid rgba($cyber-secondary, 0.3);
		box-shadow: 0 0 15px rgba($cyber-secondary, 0.2);
		transition: all 0.3s ease;

		&:hover {
			transform: scale(1.05);
			box-shadow: 0 0 20px rgba($cyber-secondary, 0.4);
		}
	}

	.cyber-monitor-item {
		background: rgba($cyber-secondary, 0.1) !important;
		border: 1px solid rgba($cyber-primary, 0.2);
		padding: 15px;
		transition: all 0.3s ease;

		&:hover {
			background: rgba($cyber-secondary, 0.2) !important;
			transform: translateY(-2px);
			box-shadow: 0 5px 15px rgba($cyber-primary, 0.2);
		}
	}

	.chart-container {
		padding: 10px;
		border-radius: 4px;
		background: rgba($cyber-bg, 0.5);
	}

	.home-card-one,
	.home-card-two,
	.home-card-three {
		.home-card-item {
			height: 130px;
			border-radius: 8px;
			transition: all ease 0.3s;
			padding: 20px;
			overflow: hidden;
		}
	}

	.home-card-two,
	.home-card-three {
		.home-card-item {
			height: 400px;
		}
	}

	@keyframes cyber-scan {
		0% {
			transform: translateX(-100%);
		}
		100% {
			transform: translateX(100%);
		}
	}

	@keyframes error-num {
		0% {
			transform: translateY(20px);
			opacity: 0;
		}
		100% {
			transform: translateY(0);
			opacity: 1;
		}
	}
}
</style>
