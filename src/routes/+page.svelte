<script lang="ts">
	import { onMount } from 'svelte';
	import PostCard from '$lib/PostCard.svelte';
	import PostComposer from '$lib/PostComposer.svelte';
	import { fetchPosts, type Post } from '$lib/api';

	let posts = $state<Post[]>([]);
	let isLoading = $state(false);
	let error = $state('');
	let nextCursor = $state<string | null>(null);
	let hasMore = $state(true);
	let sentinel: HTMLDivElement;
	let observer: IntersectionObserver | null = null;

	async function loadMore() {
		if (isLoading || !hasMore) {
			return;
		}

		isLoading = true;
		error = '';

		try {
			const page = await fetchPosts(nextCursor);
			posts = [...posts, ...page.posts];
			nextCursor = page.nextCursor;
			hasMore = page.hasMore;
		} catch {
			error = '投稿を読み込めませんでした。';
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
		void loadMore();

		observer = new IntersectionObserver(
			(entries) => {
				if (entries[0]?.isIntersecting) {
					void loadMore();
				}
			},
			{ rootMargin: '360px' }
		);

		observer.observe(sentinel);

		return () => observer?.disconnect();
	});
</script>

<section class="page-header">
	<div>
		<h1>ホーム</h1>
		<p>すべてのアカウントの投稿</p>
	</div>

	<PostComposer onCreated={handlePostCreated} />
</section>

<section class="feed" aria-label="投稿フィード">
	{#each posts as post (post.id)}
		<PostCard {post} onDeleted={handlePostDeleted} />
	{/each}

	{#if error}
		<p class="message error">{error}</p>
	{/if}

	{#if isLoading}
		<p class="message">投稿を読み込み中...</p>
	{:else if !hasMore && posts.length > 0}
		<p class="message">これ以上投稿はありません。</p>
	{:else if posts.length === 0}
		<p class="message">まだ投稿がありません。</p>
	{/if}

	<div class="sentinel" bind:this={sentinel}></div>
</section>

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

	.feed {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
		gap: 12px;
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

	.sentinel {
		grid-column: 1 / -1;
		height: 1px;
	}

	@media (max-width: 520px) {
		.page-header {
			align-items: flex-start;
		}

		h1 {
			font-size: 23px;
		}
	}
</style>
