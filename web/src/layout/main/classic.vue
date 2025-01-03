<template>
	<el-container class="layout-container flex-center cyber-theme">
		<LayoutHeader class="cyber-header" />
		<el-container class="layout-mian-height-50">
			<LayoutAside class="cyber-aside" />
			<div class="flex-center layout-backtop">
				<LayoutTagsView v-if="isTagsview" class="cyber-tags" />
				<LayoutMain ref="layoutMainRef" class="cyber-main" />
			</div>
		</el-container>
	</el-container>
</template>

<script setup lang="ts" name="layoutClassic">
import { defineAsyncComponent, computed, ref, watch, nextTick, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { storeToRefs } from 'pinia';
import { useThemeConfig } from '/@/stores/themeConfig';
import '/@/theme/cyber.scss';

// 引入组件
const LayoutAside = defineAsyncComponent(() => import('/@/layout/component/aside.vue'));
const LayoutHeader = defineAsyncComponent(() => import('/@/layout/component/header.vue'));
const LayoutMain = defineAsyncComponent(() => import('/@/layout/component/main.vue'));
const LayoutTagsView = defineAsyncComponent(() => import('/@/layout/navBars/tagsView/tagsView.vue'));

// 定义变量内容
const layoutMainRef = ref<InstanceType<typeof LayoutMain>>();
const route = useRoute();
const storesThemeConfig = useThemeConfig();
const { themeConfig } = storeToRefs(storesThemeConfig);

// 判断是否显示 tasgview
const isTagsview = computed(() => {
	return themeConfig.value.isTagsview;
});

// 重置滚动条高度，更新子级 scrollbar
const updateScrollbar = () => {
	layoutMainRef.value?.layoutMainScrollbarRef.update();
};

// 重置滚动条高度，由于组件是异步引入的
const initScrollBarHeight = () => {
	nextTick(() => {
		setTimeout(() => {
			updateScrollbar();
			layoutMainRef.value!.layoutMainScrollbarRef.wrapRef.scrollTop = 0;
		}, 500);
	});
};

// 页面加载时
onMounted(() => {
	initScrollBarHeight();
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
	.layout-mian-height-50 {
		height: calc(100% - 50px);
		.cyber-main {
			position: relative;
			overflow: hidden;
			background: var(--next-bg-main);
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
</style>
