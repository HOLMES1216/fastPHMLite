<template>
	<el-container class="layout-container cyber-theme">
		<LayoutAside class="cyber-aside" />
		<el-container class="layout-container-view h100">
			<el-scrollbar ref="layoutScrollbarRef" class="layout-backtop cyber-scrollbar">
				<LayoutHeader class="cyber-header" />
				<LayoutMain ref="layoutMainRef" class="cyber-main" />
			</el-scrollbar>
		</el-container>
	</el-container>
</template>

<script setup lang="ts" name="layoutDefaults">
import { defineAsyncComponent, watch, onMounted, nextTick, ref } from 'vue';
import { useRoute } from 'vue-router';
import { storeToRefs } from 'pinia';
import { useThemeConfig } from '/@/stores/themeConfig';
import { NextLoading } from '/@/utils/loading';
import '/@/theme/cyber.scss';

// 引入组件
const LayoutAside = defineAsyncComponent(() => import('/@/layout/component/aside.vue'));
const LayoutHeader = defineAsyncComponent(() => import('/@/layout/component/header.vue'));
const LayoutMain = defineAsyncComponent(() => import('/@/layout/component/main.vue'));

// 定义变量内容
const layoutScrollbarRef = ref<RefType>('');
const layoutMainRef = ref<InstanceType<typeof LayoutMain>>();
const route = useRoute();
const storesThemeConfig = useThemeConfig();
const { themeConfig } = storeToRefs(storesThemeConfig);

// 重置滚动条高度
const updateScrollbar = () => {
	// 更新父级 scrollbar
	layoutScrollbarRef.value.update();
	// 更新子级 scrollbar
	layoutMainRef.value!.layoutMainScrollbarRef.update();
};

// 重置滚动条高度，由于组件是异步引入的
const initScrollBarHeight = () => {
	nextTick(() => {
		setTimeout(() => {
			updateScrollbar();
			layoutScrollbarRef.value.wrapRef.scrollTop = 0;
			layoutMainRef.value!.layoutMainScrollbarRef.wrapRef.scrollTop = 0;
		}, 500);
	});
};

// 页面加载时
onMounted(() => {
	initScrollBarHeight();
	NextLoading.done(600);
});

// 监听路由的变化，切换界面时，滚动条置顶
watch(
	() => route.path,
	() => {
		initScrollBarHeight();
	}
);

// 监听 themeConfig 配置文件的变化，更新菜单 el-scrollbar 的高度
watch(
	themeConfig,
	() => {
		updateScrollbar();
	},
	{
		
		deep: true,
	}
);
</script>

<style lang="scss" scoped>
.layout-container {
	width: 100%;
	height: 100%;
	.layout-container-view {
		background: linear-gradient(135deg, #0a0e17 0%, #1a1f2c 100%);
		
		.cyber-main {
			position: relative;
			overflow: hidden;
			
			&::before {
				content: '';
				position: absolute;
				top: 0;
				left: 0;
				width: 100%;
				height: 100%;
				background: linear-gradient(135deg, rgba(0,243,255,0.1) 0%, rgba(0,81,255,0.05) 100%);
				pointer-events: none;
			}
		}
	}
}

// 自定义滚动条样式
.cyber-scrollbar {
	:deep(.el-scrollbar__bar) {
		&.is-horizontal {
			height: 6px;
			
			> div {
				background: rgba(0, 243, 255, 0.3);
				&:hover {
					background: rgba(0, 243, 255, 0.5);
				}
			}
		}
		
		&.is-vertical {
			width: 6px;
			
			> div {
				background: rgba(0, 243, 255, 0.3);
				&:hover {
					background: rgba(0, 243, 255, 0.5);
				}
			}
		}
	}
}
</style>
