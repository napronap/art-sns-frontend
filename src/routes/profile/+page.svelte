<script lang="ts">
	import { onMount } from 'svelte';
	import PostCard from '$lib/PostCard.svelte';
	import PostComposer from '$lib/PostComposer.svelte';
	import { fetchCurrentAccount, fetchProfilePosts, type Account, type Post } from '$lib/api';

	let account = $state<Account | null>(null);
	let posts = $state<Post[]>([]);
	let isLoading = $state(true);
	let error = $state('');

	async function loadProfile() {
		isLoading = true;
		error = '';

		try {
			const [accountData, postData] = await Promise.all([
				fetchCurrentAccount(),
				fetchProfilePosts()
			]);
			account = accountData;
			posts = postData;
		} catch {
			error = 'プロフィールを読み込めませんでした。';
		} finally {
			isLoading = false;
		}
	}

	function handlePostCreated(post: Post) {
		posts = [post, ...posts];
	}

	function handlePostDeleted(postId: string) {
		posts = posts.filter((post) => post.id !== postId);
	}

	onMount(() => {
		void loadProfile();
	});
</script>

<section class="page-header">
	<div>
		<h1>プロフィール</h1>
		<p>アカウント情報と自分の投稿</p>
	</div>

	<PostComposer onCreated={handlePostCreated} />
</section>

{#if isLoading}
	<p class="message">プロフィールを読み込み中...</p>
{:else if error}
	<p class="message error">{error}</p>
{:else if account}
	<section class="profile-card">
		<div class="avatar" aria-hidden="true">
			{#if account.avatarUrl}
				<img src={account.avatarUrl} alt="" />
			{:else}
				<span>{account.username.slice(0, 1).toUpperCase()}</span>
			{/if}
		</div>

		<div>
			<h2>{account.displayName ?? account.username}</h2>
			<p class="username">@{account.username}</p>
			<p>{account.email}</p>
			{#if account.bio}
				<p>{account.bio}</p>
			{/if}
		</div>
	</section>

	<section class="posts-section">
		<h2>あなたの投稿</h2>

		{#if posts.length > 0}
			<div class="feed">
				{#each posts as post (post.id)}
					<PostCard {post} onDeleted={handlePostDeleted} />
				{/each}
			</div>
		{:else}
			<p class="message">まだ投稿していません。</p>
		{/if}
	</section>
{/if}

<style>
	.page-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 14px;
		margin-bottom: 16px;
	}

	h1 {
		margin: 0;
		font-size: 26px;
	}

	.page-header p {
		margin: 4px 0 0;
		color: var(--muted);
	}

	.profile-card {
		display: grid;
		grid-template-columns: 76px 1fr;
		gap: 16px;
		padding: 18px;
		border: 1px solid var(--border);
		border-radius: 8px;
		background: var(--surface);
	}

	.avatar {
		width: 76px;
		height: 76px;
		overflow: hidden;
		border-radius: 50%;
		background: var(--brand);
		color: #ffffff;
		font-size: 28px;
		font-weight: 800;
		display: grid;
		place-items: center;
	}

	.avatar img {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.profile-card h2,
	.posts-section h2 {
		margin: 0;
		font-size: 20px;
	}

	.profile-card p {
		margin: 6px 0 0;
		color: var(--muted-strong);
	}

	.username {
		font-weight: 800;
		color: var(--muted);
	}

	.posts-section {
		margin-top: 20px;
	}

	.feed {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
		gap: 12px;
		margin-top: 12px;
	}

	.message {
		grid-column: 1 / -1;
		margin: 4px 0;
		padding: 14px;
		text-align: center;
		color: var(--muted);
	}

	.error {
		color: var(--danger);
	}

	@media (max-width: 520px) {
		.page-header {
			align-items: flex-start;
		}

		.profile-card {
			grid-template-columns: 1fr;
		}
	}
</style>
