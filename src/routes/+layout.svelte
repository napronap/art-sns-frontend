<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();

	const navItems = [
		{ label: 'Home', icon: '🏠' },
		{ label: 'Explore', icon: '🔍' },
		{ label: 'Gallery', icon: '🖼️' },
		{ label: 'Messages', icon: '✉️' },
		{ label: 'Notifications', icon: '🔔' },
	];

	const tags = ['digital', 'concept art', '3D', 'illustration', 'fan art'];
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Sora:wght@500;600;700&display=swap" rel="stylesheet" />
	<title>ArtSNS</title>
</svelte:head>

<div class="app-shell">
	<aside class="sidebar">
		<div class="brand">
			<div class="brand-mark">M</div>
			<div class="brand-copy">
				<strong>MOEfolio</strong>
				<span>soft cat vibes</span>
			</div>
		</div>

		<nav class="nav-menu">
			{#each navItems as item}
				<button type="button" class="nav-item">
					<span class="nav-icon">{item.icon}</span>
					<span>{item.label}</span>
				</button>
			{/each}
		</nav>

		<div class="sidebar-section">
			<h3>Trending</h3>
			<div class="tag-list">
				{#each tags as tag}
					<span class="tag">#{tag}</span>
				{/each}
			</div>
		</div>
	</aside>

	<main class="main-content">
		<header class="topbar">
			<div class="searchbar">
				<span>🔎</span>
				<input type="search" placeholder="Search artists, artworks, galleries..." />
			</div>

			<div class="top-actions">
				<button class="action-pill">Upload</button>
				<button class="action-icon" aria-label="Activity">★</button>
				<button class="avatar" aria-label="Profile">Y</button>
			</div>
		</header>

		<section class="hero-banner">
			<div>
				<p class="eyebrow">Discover, share, and inspire</p>
				<h1>MOEfolio: where soft cat art lives.</h1>
				<p>Explore warm galleries, dreamy portfolios, and cozy creator spaces for gentle visual storytellers.</p>
				<div class="hero-actions">
					<button class="primary">Browse feed</button>
					<button class="secondary">Explore galleries</button>
				</div>
			</div>

			<div class="hero-preview">
				<div class="preview-card preview-large">
					<img src="https://picsum.photos/seed/moefolio-featured/520/320" alt="Featured project placeholder" loading="lazy" decoding="async" />
					<div class="preview-copy">
						<span>Featured project</span>
						<h3>Catwalk Sketchbook</h3>
					</div>
				</div>
				<div class="preview-card preview-muted">
					<img src="https://picsum.photos/seed/moefolio-trending/420/260" alt="Trending gallery placeholder" loading="lazy" decoding="async" />
					<div class="preview-copy">
						<span>Trending gallery</span>
						<h3>Purrfect Pastel Collection</h3>
					</div>
				</div>
			</div>
		</section>

		<section class="content-panel">
			<div class="panel-heading">
				<div>
					<p class="section-label">Home feed</p>
					<h2>Latest artwork from your network</h2>
				</div>
				<button class="sort-button">Latest</button>
			</div>
			{@render children()}
		</section>
	</main>

	<aside class="rightpanel">
		<div class="panel-card">
			<h3>Featured muse</h3>
			<div class="artist-suggest">
				<div class="artist-avatar">M</div>
				<div>
					<strong>MoonPaw</strong>
					<span>Cozy illustration · 46k followers</span>
				</div>
			</div>
			<button class="follow-btn">Follow</button>
		</div>

		<div class="panel-card">
			<h3>Community highlights</h3>
			<ul>
				<li>New gallery releases</li>
				<li>Live critique session</li>
				<li>Weekly theme challenge</li>
			</ul>
		</div>
	</aside>
</div>

<style>
	:global(body) {
		margin: 0;
		font-family: 'Poppins', Inter, system-ui, sans-serif;
		background: linear-gradient(180deg, #f6f5ff 0%, #eef2ff 100%);
		color: #27284a;
	}

	:global(*) {
		box-sizing: border-box;
	}

	.app-shell {
		display: grid;
		grid-template-columns: 280px minmax(0, 1fr) 300px;
		min-height: 100vh;
		gap: 24px;
		padding: 24px;
	}

	.sidebar,
	.rightpanel,
	.hero-banner,
	.panel-card {
		background: rgba(255, 255, 255, 0.9);
		border: 1px solid rgba(141, 130, 255, 0.16);
		border-radius: 32px;
		box-shadow: 0 20px 45px rgba(95, 80, 205, 0.08);
	}

	.sidebar {
		display: flex;
		flex-direction: column;
		gap: 26px;
		padding: 26px;
	}

	.brand {
		display: flex;
		align-items: center;
		gap: 16px;
	}

	.brand-mark {
		width: 50px;
		height: 50px;
		border-radius: 18px;
		background: linear-gradient(135deg, #d4b1ff, #f7c3f6);
		display: grid;
		place-items: center;
		font-size: 1.2rem;
		font-weight: 800;
		color: #3d2a70;
	}

	.brand-copy strong {
		display: block;
		font-size: 1.12rem;
		color: #262749;
	}

	.brand-copy span {
		color: #7c72a2;
		font-size: 0.92rem;
	}

	.nav-menu {
		display: grid;
		gap: 10px;
	}

	.nav-item {
		width: 100%;
		border: none;
		background: #f7f4ff;
		color: inherit;
		text-align: left;
		padding: 14px 18px;
		border-radius: 20px;
		display: flex;
		align-items: center;
		gap: 14px;
		cursor: pointer;
		transition: background 0.2s, transform 0.2s, box-shadow 0.2s;
	}

	.nav-item:hover,
	.nav-item:focus-visible {
		background: #ede9ff;
		transform: translateY(-1px);
		box-shadow: 0 10px 26px rgba(138, 104, 216, 0.12);
	}

	.nav-icon {
		width: 36px;
		height: 36px;
		display: grid;
		place-items: center;
		background: #f0ebff;
		border-radius: 16px;
		color: #6150a9;
	}

	.nav-item span:last-child {
		font-family: 'Sora', sans-serif;
		font-weight: 600;
		font-size: 0.98rem;
		letter-spacing: 0.02em;
		color: #3f336a;
	}

	.sidebar-section h3 {
		margin: 0 0 12px;
		color: #7f77a5;
		font-size: 0.85rem;
		text-transform: uppercase;
		letter-spacing: 0.12em;
	}

	.tag-list {
		display: flex;
		flex-wrap: wrap;
		gap: 10px;
	}

	.tag {
		display: inline-flex;
		padding: 8px 12px;
		background: #f3eeff;
		border: 1px solid #e6ddff;
		border-radius: 999px;
		color: #6c5fa8;
		font-size: 0.9rem;
	}

	.main-content {
		display: flex;
		flex-direction: column;
		gap: 24px;
	}

	.topbar {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 16px;
	}

	.searchbar {
		flex: 1;
		display: flex;
		align-items: center;
		gap: 12px;
		padding: 16px 18px;
		background: #f6f3ff;
		border: 1px solid #e3ddff;
		border-radius: 22px;
	}

	.searchbar input {
		width: 100%;
		border: none;
		outline: none;
		background: transparent;
		color: #3b3560;
		font-size: 0.96rem;
	}

	.top-actions {
		display: flex;
		gap: 12px;
		align-items: center;
	}

	.action-pill,
	.action-icon,
	.avatar,
	.follow-btn,
	.sort-button {
		border: none;
		cursor: pointer;
		border-radius: 18px;
		transition: transform 0.2s, background 0.2s;
	}

	.action-pill {
		padding: 12px 18px;
		background: linear-gradient(90deg, #d6befd, #f8b5ef);
		color: #3f2d67;
		font-family: 'Sora', 'Poppins', sans-serif;
		font-weight: 600;
		letter-spacing: 0.02em;
	}

	.action-pill:hover {
		transform: translateY(-1px);
	}

	.action-icon {
		width: 48px;
		height: 48px;
		display: grid;
		place-items: center;
		background: #f3eeff;
		color: #5b4595;
		font-size: 1.1rem;
	}

	.avatar {
		width: 48px;
		height: 48px;
		border-radius: 50%;
		background: #d8c7ff;
		color: #382f64;
		font-weight: 700;
	}

	.hero-banner {
		display: grid;
		grid-template-columns: 1.5fr 1fr;
		gap: 24px;
		padding: 36px;
		min-height: 280px;
	}

	.eyebrow {
		margin: 0 0 12px;
		text-transform: uppercase;
		letter-spacing: 0.22em;
		color: #7f6dde;
		font-size: 0.75rem;
	}

	.hero-banner h1 {
		margin: 0 0 16px;
		font-size: clamp(2rem, 3vw, 3.25rem);
		line-height: 1.05;
		color: #2b2751;
	}

	.hero-banner p {
		margin: 0 0 22px;
		max-width: 38rem;
		color: #6f6794;
	}

	.hero-actions {
		display: flex;
		gap: 12px;
		flex-wrap: wrap;
	}

	.primary,
	.secondary {
		padding: 14px 22px;
		border-radius: 18px;
		font-family: 'Sora', 'Poppins', sans-serif;
		font-weight: 600;
		letter-spacing: 0.02em;
	}

	.primary {
		background: linear-gradient(90deg, #bea0ff, #dca7f0);
		color: #32265d;
	}

	.secondary {
		background: #fff;
		color: #5e5390;
		border: 1px solid #e8e1ff;
	}

	.hero-preview {
		display: grid;
		gap: 16px;
	}

	.preview-card {
		position: relative;
		min-height: 180px;
		border-radius: 28px;
		overflow: hidden;
		display: grid;
		place-items: end;
		color: #3e3460;
		font-weight: 700;
		background: #f7f2ff;
	}

	.preview-card img {
		width: 100%;
		height: 100%;
		object-fit: cover;
		display: block;
	}

	.preview-copy {
		position: absolute;
		left: 0;
		bottom: 0;
		width: 100%;
		padding: 18px 20px;
		background: linear-gradient(180deg, transparent 0%, rgba(24, 18, 54, 0.68) 100%);
		color: #fff;
	}

	.preview-copy span {
		display: block;
		font-size: 0.85rem;
		text-transform: uppercase;
		letter-spacing: 0.14em;
		margin-bottom: 8px;
		color: rgba(255, 255, 255, 0.85);
	}

	.preview-copy h3 {
		margin: 0;
		font-size: 1.25rem;
	}

	.preview-card.preview-muted {
		min-height: 160px;
	}

	.preview-card.preview-large {
		min-height: 260px;
	}

	.content-panel {
		display: flex;
		flex-direction: column;
		gap: 18px;
	}

	.panel-heading {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 16px;
	}

	.section-label {
		margin: 0;
		color: #7e759e;
		text-transform: uppercase;
		letter-spacing: 0.12em;
		font-size: 0.82rem;
	}

	.panel-heading h2 {
		margin: 0;
		font-size: 1.65rem;
		color: #2b2751;
	}

	.sort-button {
		padding: 12px 18px;
		background: #f6f3ff;
		color: #5f5595;
	}

	.rightpanel {
		display: flex;
		flex-direction: column;
		gap: 20px;
	}

	.panel-card {
		padding: 24px;
		display: flex;
		flex-direction: column;
		gap: 18px;
	}

	.artist-suggest {
		display: flex;
		gap: 14px;
		align-items: center;
	}

	.artist-avatar {
		width: 56px;
		height: 56px;
		border-radius: 18px;
		background: linear-gradient(135deg, #f1c7ff, #c8d4ff);
		display: grid;
		place-items: center;
		font-weight: 800;
		color: #4f3d7c;
	}

	.follow-btn {
		padding: 12px 18px;
		background: linear-gradient(135deg, #c0a1ff, #c7d6ff);
		color: #3f335d;
		font-weight: 700;
	}

	.rightpanel h3,
	.sidebar-section h3,
	.panel-heading h2 {
		margin: 0;
	}

	.rightpanel ul {
		margin: 0;
		padding: 0;
		list-style: none;
		display: grid;
		gap: 10px;
	}

	.rightpanel li {
		padding-left: 10px;
		position: relative;
		color: #7d729f;
	}

	.rightpanel li::before {
		content: '•';
		position: absolute;
		left: 0;
		color: #9c8aff;
	}

	@media (max-width: 1200px) {
		.app-shell {
			grid-template-columns: 1fr;
		}

		.rightpanel {
			order: 3;
		}
	}

	@media (max-width: 900px) {
		.hero-banner {
			grid-template-columns: 1fr;
		}

		.topbar {
			flex-direction: column;
			align-items: stretch;
		}

		.searchbar {
			width: 100%;
		}

		.app-shell {
			padding: 16px;
			gap: 16px;
		}
	}
</style>