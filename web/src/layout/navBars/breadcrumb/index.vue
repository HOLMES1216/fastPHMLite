<template>
	<div class="layout-navbars-breadcrumb-index cyber-breadcrumb">
		<Logo v-if="setIsShowLogo" class="cyber-logo" />
		<Breadcrumb class="cyber-nav" />
		<Horizontal :menuList="state.menuList" v-if="isLayoutTransverse" class="cyber-horizontal" />
		<User class="cyber-user" />
	</div>
</template>

<script setup lang="ts" name="layoutBreadcrumbIndex">
import { defineAsyncComponent, computed, reactive, onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import { storeToRefs } from 'pinia';
import { useRoutesList } from '/@/stores/routesList';
import { useThemeConfig } from '/@/stores/themeConfig';
import mittBus from '/@/utils/mitt';

// 引入组件
const Breadcrumb = defineAsyncComponent(() => import('/@/layout/navBars/breadcrumb/breadcrumb.vue'));
const User = defineAsyncComponent(() => import('/@/layout/navBars/breadcrumb/user.vue'));
const Logo = defineAsyncComponent(() => import('/@/layout/logo/index.vue'));
const Horizontal = defineAsyncComponent(() => import('/@/layout/navMenu/horizontal.vue'));

// 定义变量内容
const stores = useRoutesList();
const storesThemeConfig = useThemeConfig();
const { themeConfig } = storeToRefs(storesThemeConfig);
const { routesList } = storeToRefs(stores);
const route = useRoute();
const state = reactive({
	menuList: [] as RouteItems,
});

// 设置 logo 显示/隐藏
const setIsShowLogo = computed(() => {
	let { isShowLogo, layout } = themeConfig.value;
	return (isShowLogo && layout === 'classic') || (isShowLogo && layout === 'transverse');
});
// 设置是否显示横向导航菜单
const isLayoutTransverse = computed(() => {
	let { layout, isClassicSplitMenu } = themeConfig.value;
	return layout === 'transverse' || (isClassicSplitMenu && layout === 'classic');
});
// 设置/过滤路由（非静态路由/是否显示在菜单中）
const setFilterRoutes = () => {
	let { layout, isClassicSplitMenu } = themeConfig.value;
	if (layout === 'classic' && isClassicSplitMenu) {
		state.menuList = delClassicChildren(filterRoutesFun(routesList.value));
		const resData = setSendClassicChildren(route.path);
		mittBus.emit('setSendClassicChildren', resData);
	} else {
		state.menuList = filterRoutesFun(routesList.value);
	}
};
// 设置了分割菜单时，删除底下 children
const delClassicChildren = <T extends ChilType>(arr: T[]): T[] => {
	arr.map((v: T) => {
		if (v.children) delete v.children;
	});
	return arr;
};
// 路由过滤递归函数
const filterRoutesFun = <T extends RouteItem>(arr: T[]): T[] => {
	return arr
		.filter((item: T) => !item.meta?.isHide)
		.map((item: T) => {
			item = Object.assign({}, item);
			if (item.children) item.children = filterRoutesFun(item.children);
			return item;
		});
};
// 传送当前子级数据到菜单中
const setSendClassicChildren = (path: string) => {
	const currentPathSplit = path.split('/');
	let currentData: MittMenu = { children: [] };
	filterRoutesFun(routesList.value).map((v: RouteItem, k: number) => {
		if (v.path === `/${currentPathSplit[1]}`) {
			v['k'] = k;
			currentData['item'] = { ...v };
			currentData['children'] = [{ ...v }];
			if (v.children) currentData['children'] = v.children;
		}
	});
	return currentData;
};
// 页面加载时
onMounted(() => {
	setFilterRoutes();
	mittBus.on('getBreadcrumbIndexSetFilterRoutes', () => {
		setFilterRoutes();
	});
});
// 页面卸载时
onUnmounted(() => {
	mittBus.off('getBreadcrumbIndexSetFilterRoutes', () => {});
});
</script>

<style scoped lang="scss">
.cyber-breadcrumb {
	height: 50px;
	display: flex;
	align-items: center;
	background: rgba(16, 20, 31, 0.8);
	backdrop-filter: blur(10px);
	border-bottom: 1px solid rgba(0, 243, 255, 0.3);
	position: relative;
	z-index: 5;

	&::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		height: 1px;
		background: linear-gradient(90deg, transparent, rgba(0, 243, 255, 0.5), transparent);
		animation: cyber-scan 4s linear infinite;
	}

	:deep(.cyber-nav) {
		flex: 1;
		padding: 0 20px;

		.el-breadcrumb {
			.el-breadcrumb__item {
				.el-breadcrumb__inner {
					color: rgba(255, 255, 255, 0.7);
					transition: all 0.3s ease;
					
					&:hover {
						color: #00f3ff;
						text-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
					}
					
					&.is-link {
						color: rgba(255, 255, 255, 0.5);
						
						&:hover {
							color: #00f3ff;
							text-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
						}
					}
				}
				
				.el-breadcrumb__separator {
					color: rgba(255, 255, 255, 0.3);
				}
			}
		}
	}

	:deep(.cyber-horizontal) {
		.el-menu {
			background: transparent;
			border: none;

			.el-menu-item, .el-sub-menu__title {
				color: rgba(255, 255, 255, 0.7);
				background: transparent;
				border-bottom: 2px solid transparent;
				transition: all 0.3s ease;

				&:hover, &.is-active {
					color: #00f3ff;
					background: rgba(0, 243, 255, 0.1);
					border-bottom-color: #00f3ff;
					text-shadow: 0 0 10px rgba(0, 243, 255, 0.5);

					&::after {
						content: '';
						position: absolute;
						bottom: 0;
						left: 0;
						right: 0;
						height: 2px;
						background: #00f3ff;
						box-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
					}
				}
			}
		}
	}

	:deep(.cyber-user) {
		margin-right: 15px;
		
		.el-dropdown {
			color: rgba(255, 255, 255, 0.8);
			
			&:hover {
				color: #00f3ff;
				text-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
			}
		}

		.user-icon {
			width: 35px;
			height: 35px;
			border: 2px solid rgba(0, 243, 255, 0.3);
			border-radius: 50%;
			transition: all 0.3s ease;
			
			&:hover {
				border-color: #00f3ff;
				box-shadow: 0 0 15px rgba(0, 243, 255, 0.5);
				transform: scale(1.05);
			}
		}
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
</style>
