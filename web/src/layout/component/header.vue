<template>
	<el-header class="layout-header cyber-header" v-show="!isTagsViewCurrenFull">
		<NavBarsIndex />
	</el-header>
</template>

<script setup lang="ts" name="layoutHeader">
import { defineAsyncComponent } from 'vue';
import { storeToRefs } from 'pinia';
import { useTagsViewRoutes } from '/@/stores/tagsViewRoutes';

// 引入组件
const NavBarsIndex = defineAsyncComponent(() => import('/@/layout/navBars/index.vue'));

// 定义变量内容
const storesTagsViewRoutes = useTagsViewRoutes();
const { isTagsViewCurrenFull } = storeToRefs(storesTagsViewRoutes);
</script>

<style lang="scss" scoped>
.layout-header {
	height: 55px;
	padding: 0;
	background: rgba(16, 20, 31, 0.8);
	border-bottom: 1px solid rgba(0, 243, 255, 0.3);
	backdrop-filter: blur(10px);
	position: relative;
	z-index: 999;
	transition: all 0.3s ease;

	&::before {
		content: '';
		position: absolute;
		bottom: -1px;
		left: 0;
		right: 0;
		height: 1px;
		background: linear-gradient(90deg, transparent, rgba(0, 243, 255, 0.5), transparent);
		animation: cyber-scan 4s linear infinite;
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
