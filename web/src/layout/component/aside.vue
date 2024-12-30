<template>
	<div class="h100" v-show="!isTagsViewCurrenFull">
		<el-aside class="layout-aside cyber-aside" :class="setCollapseStyle">
			<Logo v-if="setShowLogo" class="cyber-logo" />
			<el-scrollbar class="flex-auto cyber-scrollbar" ref="layoutAsideScrollbarRef" @mouseenter="onAsideEnterLeave(true)" @mouseleave="onAsideEnterLeave(false)">
				<Vertical :menuList="state.menuList" />
			</el-scrollbar>
		</el-aside>
	</div>
</template>

<script setup lang="ts" name="layoutAside">
import { defineAsyncComponent, reactive, computed, watch, onBeforeMount, ref } from 'vue';
import { storeToRefs } from 'pinia';
import pinia from '/@/stores/index';
import { useRoutesList } from '/@/stores/routesList';
import { useThemeConfig } from '/@/stores/themeConfig';
import { useTagsViewRoutes } from '/@/stores/tagsViewRoutes';
import mittBus from '/@/utils/mitt';

// 引入组件
const Logo = defineAsyncComponent(() => import('/@/layout/logo/index.vue'));
const Vertical = defineAsyncComponent(() => import('/@/layout/navMenu/vertical.vue'));

// 定义变量内容
const layoutAsideScrollbarRef = ref();
const stores = useRoutesList();
const storesThemeConfig = useThemeConfig();
const storesTagsViewRoutes = useTagsViewRoutes();
const { routesList } = storeToRefs(stores);
const { themeConfig } = storeToRefs(storesThemeConfig);
const { isTagsViewCurrenFull } = storeToRefs(storesTagsViewRoutes);
const state = reactive<AsideState>({
	menuList: [],
	clientWidth: 0,
});

// 设置菜单展开/收起时的宽度
const setCollapseStyle = computed(() => {
	const { layout, isCollapse, menuBar } = themeConfig.value;
	const asideBrTheme = ['#FFFFFF', '#FFF', '#fff', '#ffffff'];
	const asideBrColor = asideBrTheme.includes(menuBar) ? 'layout-el-aside-br-color' : '';
	// 判断是否是手机端
	if (state.clientWidth <= 1000) {
		if (isCollapse) {
			document.body.setAttribute('class', 'el-popup-parent--hidden');
			const asideEle = document.querySelector('.layout-container') as HTMLElement;
			const modeDivs = document.createElement('div');
			modeDivs.setAttribute('class', 'layout-aside-mobile-mode');
			asideEle.appendChild(modeDivs);
			modeDivs.addEventListener('click', closeLayoutAsideMobileMode);
			return [asideBrColor, 'layout-aside-mobile', 'layout-aside-mobile-open'];
		} else {
			// 关闭弹窗
			closeLayoutAsideMobileMode();
			return [asideBrColor, 'layout-aside-mobile', 'layout-aside-mobile-close'];
		}
	} else {
		if (layout === 'columns') {
			// 分栏布局，菜单收起时宽度给 1px
			if (isCollapse) return [asideBrColor, 'layout-aside-pc-1'];
			else return [asideBrColor, 'layout-aside-pc-220'];
		} else {
			// 其它布局给 64px
			if (isCollapse) return [asideBrColor, 'layout-aside-pc-64'];
			else return [asideBrColor, 'layout-aside-pc-220'];
		}
	}
});
// 设置显示/隐藏 logo
const setShowLogo = computed(() => {
	let { layout, isShowLogo } = themeConfig.value;
	return (isShowLogo && layout === 'defaults') || (isShowLogo && layout === 'columns');
});
// 关闭移动端蒙版
const closeLayoutAsideMobileMode = () => {
	const el = document.querySelector('.layout-aside-mobile-mode');
	el?.setAttribute('style', 'animation: error-img-two 0.3s');
	setTimeout(() => {
		el?.parentNode?.removeChild(el);
	}, 300);
	const clientWidth = document.body.clientWidth;
	if (clientWidth < 1000) themeConfig.value.isCollapse = false;
	document.body.setAttribute('class', '');
};
// 设置/过滤路由（非静态路由/是否显示在菜单中）
const setFilterRoutes = () => {
	if (themeConfig.value.layout === 'columns') return false;
	state.menuList = filterRoutesFun(routesList.value);
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
// 设置菜单导航是否固定（移动端）
const initMenuFixed = (clientWidth: number) => {
	state.clientWidth = clientWidth;
};
// 鼠标移入、移出
const onAsideEnterLeave = (bool: Boolean) => {
	let { layout } = themeConfig.value;
	if (layout !== 'columns') return false;
	if (!bool) mittBus.emit('restoreDefault');
	stores.setColumnsMenuHover(bool);
};
// 页面加载前
onBeforeMount(() => {
	initMenuFixed(document.body.clientWidth);
	setFilterRoutes();
	// 此界面不需要取消监听(mittBus.off('setSendColumnsChildren))
	// 因为切换布局时有的监听需要使用，取消了监听，某些操作将不生效
	mittBus.on('setSendColumnsChildren', (res: MittMenu) => {
		state.menuList = res.children;
	});
	mittBus.on('setSendClassicChildren', (res: MittMenu) => {
		let { layout, isClassicSplitMenu } = themeConfig.value;
		if (layout === 'classic' && isClassicSplitMenu) {
			state.menuList = [];
			state.menuList = res.children;
		}
	});
	mittBus.on('getBreadcrumbIndexSetFilterRoutes', () => {
		setFilterRoutes();
	});
	mittBus.on('layoutMobileResize', (res: LayoutMobileResize) => {
		initMenuFixed(res.clientWidth);
		closeLayoutAsideMobileMode();
	});
});
// 监听 themeConfig 配置文件的变化，更新菜单 el-scrollbar 的高度
watch(themeConfig.value, (val) => {
	if (val.isShowLogoChange !== val.isShowLogo) {
		if (layoutAsideScrollbarRef.value) layoutAsideScrollbarRef.value.update();
	}
});
// 监听 pinia 值的变化，动态赋值给菜单中
watch(
	pinia.state,
	(val) => {
		let { layout, isClassicSplitMenu } = val.themeConfig.themeConfig;
		if (layout === 'classic' && isClassicSplitMenu) return false;
		setFilterRoutes();
	},
	{
		deep: true,
	}
);
</script>

<style lang="scss" scoped>
.layout-aside {
	background: rgba(16, 20, 31, 0.8);
	border-right: 1px solid rgba(0, 243, 255, 0.3);
	backdrop-filter: blur(10px);
	position: relative;
	overflow: hidden;
	transition: all 0.3s ease;
	z-index: 10;

	&::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		right: -1px;
		width: 1px;
		background: linear-gradient(to bottom, transparent, rgba(0, 243, 255, 0.5), transparent);
		animation: cyber-scan-vertical 4s linear infinite;
	}

	&.layout-aside-pc-220 {
		:deep(.el-menu) {
			border: none;
			background: transparent;

			.el-menu-item, .el-sub-menu__title {
				color: rgba(255, 255, 255, 0.8);
				background: transparent;

				&:hover {
					color: #00f3ff;
					background: rgba(0, 243, 255, 0.1);
				}

				&.is-active {
					color: #00f3ff;
					background: rgba(0, 243, 255, 0.15);
					border-right: 2px solid #00f3ff;
					box-shadow: inset 0 0 15px rgba(0, 243, 255, 0.1);

					&::before {
						content: '';
						position: absolute;
						left: 0;
						top: 0;
						bottom: 0;
						width: 2px;
						background: #00f3ff;
						box-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
					}
				}

				i {
					color: inherit;
					transition: all 0.3s ease;
				}
			}

			.el-sub-menu {
				.el-menu {
					background: rgba(0, 0, 0, 0.2);
				}
			}
		}
	}

	&.layout-aside-pc-64 {
		:deep(.el-menu) {
			border: none;
			background: transparent;

			.el-menu-item, .el-sub-menu__title {
				display: flex;
				justify-content: center;
				align-items: center;
				
				i {
					margin: 0;
				}
			}
		}
	}
}

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

@keyframes cyber-scan-vertical {
	0% {
		transform: translateY(-100%);
	}
	100% {
		transform: translateY(100%);
	}
}
</style>
