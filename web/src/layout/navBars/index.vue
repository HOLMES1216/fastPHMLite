<template>
	<div class="layout-navbars-container cyber-navbars">
		<BreadcrumbIndex class="cyber-breadcrumb" />
		<TagsView v-if="setShowTagsView" class="cyber-tags" />
	</div>
</template>

<script setup lang="ts" name="layoutNavBars">
import { defineAsyncComponent, computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useThemeConfig } from '/@/stores/themeConfig';

// 引入组件
const BreadcrumbIndex = defineAsyncComponent(() => import('/@/layout/navBars/breadcrumb/index.vue'));
const TagsView = defineAsyncComponent(() => import('/@/layout/navBars/tagsView/tagsView.vue'));

// 定义变量内容
const storesThemeConfig = useThemeConfig();
const { themeConfig } = storeToRefs(storesThemeConfig);

// 是否显示 tagsView
const setShowTagsView = computed(() => {
	let { layout, isTagsview } = themeConfig.value;
	return layout !== 'classic' && isTagsview;
});
</script>

<style scoped lang="scss">
.cyber-navbars {
	display: flex;
	flex-direction: column;
	width: 100%;
	height: 100%;
	background: rgba(16, 20, 31, 0.8);
	backdrop-filter: blur(10px);
	position: relative;
	z-index: 4;

	&::after {
		content: '';
		position: absolute;
		bottom: 0;
		left: 0;
		right: 0;
		height: 1px;
		background: linear-gradient(90deg, transparent, rgba(0, 243, 255, 0.3), transparent);
	}

	:deep(.cyber-breadcrumb) {
		padding: 0 15px;
		height: 50px;
		display: flex;
		align-items: center;
		
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

	:deep(.cyber-tags) {
		border-top: 1px solid rgba(0, 243, 255, 0.1);
		background: rgba(16, 20, 31, 0.6);
		
		.tags-wrap {
			.el-scrollbar__wrap {
				.el-scrollbar__view {
					.tags-view-item {
						background: rgba(0, 243, 255, 0.05);
						border: 1px solid rgba(0, 243, 255, 0.2);
						color: rgba(255, 255, 255, 0.7);
						transition: all 0.3s ease;
						
						&:hover, &.is-active {
							background: rgba(0, 243, 255, 0.15);
							border-color: rgba(0, 243, 255, 0.5);
							color: #00f3ff;
							box-shadow: 0 0 10px rgba(0, 243, 255, 0.3);
							
							&::before {
								content: '';
								position: absolute;
								bottom: -1px;
								left: 0;
								right: 0;
								height: 1px;
								background: #00f3ff;
								box-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
							}
						}
					}
				}
			}
		}
	}
}
</style>
