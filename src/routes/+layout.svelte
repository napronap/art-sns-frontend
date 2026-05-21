<script lang="ts">
	import { onMount } from 'svelte';
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();

	type Theme = 'light' | 'dark';

	let theme = $state<Theme>('light');

	function applyTheme(nextTheme: Theme) {
		if (typeof document === 'undefined') {
			return;
		}

		document.documentElement.dataset.theme = nextTheme;
		localStorage.setItem('theme', nextTheme);
	}

	function setTheme(nextTheme: Theme) {
		theme = nextTheme;
		applyTheme(nextTheme);
	}

	function toggleTheme() {
		setTheme(theme === 'dark' ? 'light' : 'dark');
	}

	onMount(() => {
		const savedTheme = localStorage.getItem('theme');
		const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
		const initialTheme =
			savedTheme === 'dark' || savedTheme === 'light' ? savedTheme : prefersDark ? 'dark' : 'light';

		setTheme(initialTheme);
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>アートSNS</title>
</svelte:head>

<div class="app-shell">
	<header class="topbar">
		<a class="brand" href="/">アートSNS</a>
		<div class="topbar-actions">
			<nav aria-label="メインナビゲーション">
				<a href="/">ホーム</a>
				<a href="/profile">プロフィール</a>
			</nav>

			<button
				class="theme-toggle"
				type="button"
				onclick={toggleTheme}
				aria-pressed={theme === 'dark'}
				aria-label={theme === 'dark' ? 'ライトモードに切り替え' : 'ダークモードに切り替え'}
			>
				{theme === 'dark' ? 'ライト' : 'ダーク'}
			</button>
		</div>
	</header>

	<main>
		{@render children()}
	</main>
</div>

<style>
	:global(:root) {
		color-scheme: light;
		--page-bg: #f4f7f8;
		--surface: #ffffff;
		--surface-soft: #edf4f5;
		--surface-muted: #e7eef1;
		--border: #d8e0e4;
		--border-strong: #c8d3d8;
		--text: #111827;
		--muted: #647481;
		--muted-strong: #40515f;
		--brand: #0f766e;
		--brand-hover: #0b5f59;
		--danger: #b42318;
		--focus: #99d5cf;
		--overlay: rgba(17, 24, 39, 0.42);
		--shadow: 0 20px 50px rgba(17, 24, 39, 0.22);
	}

	:global(html[data-theme='dark']) {
		color-scheme: dark;
		--page-bg: #0f1419;
		--surface: #161d24;
		--surface-soft: #1d2a32;
		--surface-muted: #24323c;
		--border: #2b3a44;
		--border-strong: #3b4d59;
		--text: #e8eef2;
		--muted: #9baab4;
		--muted-strong: #c4ced5;
		--brand: #2bb9a8;
		--brand-hover: #36d0bd;
		--danger: #ff8a80;
		--focus: #56cfc0;
		--overlay: rgba(0, 0, 0, 0.62);
		--shadow: 0 20px 50px rgba(0, 0, 0, 0.42);
	}

	:global(*) {
		box-sizing: border-box;
	}

	:global(html) {
		background: var(--page-bg);
	}

	:global(body) {
		margin: 0;
		font-family:
			Inter,
			'Noto Sans JP',
			'Yu Gothic',
			Meiryo,
			ui-sans-serif,
			system-ui,
			-apple-system,
			BlinkMacSystemFont,
			'Segoe UI',
			sans-serif;
		background: var(--page-bg);
		color: var(--text);
	}

	:global(a) {
		color: inherit;
		text-decoration: none;
	}

	.app-shell {
		min-height: 100vh;
	}

	.topbar {
		position: sticky;
		top: 0;
		z-index: 20;
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 16px;
		padding: 14px 18px;
		border-bottom: 1px solid var(--border);
		background: var(--surface);
	}

	.brand {
		font-size: 20px;
		font-weight: 800;
	}

	nav {
		display: flex;
		gap: 8px;
	}

	.topbar-actions {
		display: flex;
		align-items: center;
		gap: 10px;
	}

	nav a {
		padding: 8px 10px;
		border-radius: 8px;
		font-size: 14px;
		font-weight: 700;
		color: var(--muted-strong);
	}

	nav a:hover {
		background: var(--surface-soft);
		color: var(--text);
	}

	.theme-toggle {
		border: 1px solid var(--border);
		border-radius: 8px;
		background: var(--surface-muted);
		color: var(--muted-strong);
		cursor: pointer;
		font: inherit;
		font-size: 13px;
		font-weight: 800;
		padding: 8px 10px;
	}

	.theme-toggle:hover {
		background: var(--surface-soft);
		color: var(--text);
	}

	main {
		width: min(760px, 100%);
		margin: 0 auto;
		padding: 18px 14px 40px;
	}

	@media (max-width: 520px) {
		.topbar {
			align-items: flex-start;
		}

		.topbar-actions {
			flex-wrap: wrap;
			justify-content: flex-end;
		}
	}
</style>
