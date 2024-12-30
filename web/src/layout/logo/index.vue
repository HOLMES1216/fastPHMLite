<template>
	<div class="layout-logo cyber-logo" v-if="setShowLogo" @click="onThemeConfigChange">
		<img :src="siteLogo" class="layout-logo-medium-img" />
		<span class="cyber-title">{{ getSystemConfig['login.site_title'] || themeConfig.globalTitle }}</span>
	</div>
	<div class="layout-logo-size cyber-logo-small" v-else @click="onThemeConfigChange">
		<img :src="siteLogo" class="layout-logo-size-img" />
	</div>
</template>

<script setup lang="ts" name="layoutLogo">
import { computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useThemeConfig } from '/@/stores/themeConfig';
import logoMini from '/@/assets/logo-mini.svg';
import { SystemConfigStore } from "/@/stores/systemConfig";
import _ from "lodash-es";
// 定义变量内容
const storesThemeConfig = useThemeConfig();
const { themeConfig } = storeToRefs(storesThemeConfig);

// 设置 logo 的显示。classic 经典布局默认显示 logo
const setShowLogo = computed(() => {
	let { isCollapse, layout } = themeConfig.value;
	return !isCollapse || layout === 'classic' || document.body.clientWidth < 1000;
});
// logo 点击实现菜单展开/收起
const onThemeConfigChange = () => {
	if (themeConfig.value.layout === 'transverse') return false;
	themeConfig.value.isCollapse = !themeConfig.value.isCollapse;
};

const systemConfigStore = SystemConfigStore()
const { systemConfig } = storeToRefs(systemConfigStore)
const getSystemConfig = computed(() => {
	return systemConfig.value
})

const siteLogo = computed(() => {
	if (!_.isEmpty(getSystemConfig.value['login.site_logo'])) {
		return getSystemConfig.value['login.site_logo']
	}
	return logoMini
});

</script>

<style scoped lang="scss">
.cyber-logo {
	width: 220px;
	height: 50px;
	display: flex;
	align-items: center;
	justify-content: center;
	background: rgba(16, 20, 31, 0.8);
	border-bottom: 1px solid rgba(0, 243, 255, 0.3);
	color: #00f3ff;
	font-size: 16px;
	cursor: pointer;
	position: relative;
	overflow: hidden;
	transition: all 0.3s ease;

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

	.cyber-title {
		white-space: nowrap;
		display: inline-block;
		color: #00f3ff;
		text-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
		font-weight: bold;
		letter-spacing: 1px;
		transition: all 0.3s ease;
	}

	.layout-logo-medium-img {
		width: 40px;
		margin-right: 10px;
		filter: drop-shadow(0 0 5px rgba(0, 243, 255, 0.5));
		transition: all 0.3s ease;
	}

	&:hover {
		background: rgba(0, 243, 255, 0.1);

		.cyber-title {
			text-shadow: 0 0 15px rgba(0, 243, 255, 0.8);
			transform: scale(1.05);
		}

		.layout-logo-medium-img {
			filter: drop-shadow(0 0 8px rgba(0, 243, 255, 0.8));
			transform: scale(1.1);
		}
	}
}

.cyber-logo-small {
	width: 64px;
	height: 50px;
	display: flex;
	align-items: center;
	justify-content: center;
	background: rgba(16, 20, 31, 0.8);
	border-bottom: 1px solid rgba(0, 243, 255, 0.3);
	cursor: pointer;
	position: relative;
	overflow: hidden;
	transition: all 0.3s ease;

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

	.layout-logo-size-img {
		width: 35px;
		filter: drop-shadow(0 0 5px rgba(0, 243, 255, 0.5));
		transition: all 0.3s ease;
	}

	&:hover {
		background: rgba(0, 243, 255, 0.1);

		.layout-logo-size-img {
			filter: drop-shadow(0 0 8px rgba(0, 243, 255, 0.8));
			transform: scale(1.1);
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
