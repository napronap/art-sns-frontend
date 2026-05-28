<script lang="ts">
	import { deletePost, type Post } from '$lib/api';

	let { post, onDeleted }: { post: Post; onDeleted?: (postId: string) => void } = $props();

	let isDeleting = $state(false);
	let deleteError = $state('');

	function formatDate(value: string) {
		const date = new Date(value);

		if (Number.isNaN(date.getTime())) {
			return '';
		}

		return new Intl.DateTimeFormat('ja-JP', {
			dateStyle: 'short',
			timeStyle: 'short'
		}).format(date);
	}

	async function handleDelete() {
		if (isDeleting) {
			return;
		}

		if (!confirm('この投稿を削除しますか？')) {
			return;
		}

		isDeleting = true;
		deleteError = '';

		try {
			await deletePost(post.id);
			onDeleted?.(post.id);
		} catch (error) {
			console.error('Failed to delete post.', error);
			deleteError = '削除できませんでした。';
		} finally {
			isDeleting = false;
		}
	}
</script>

<article class="post">
	<img class="post-image" src={post.imageUrl} alt={post.text} loading="lazy" />

	<div class="body">
		<header>
			<div class="avatar" aria-hidden="true">
				{#if post.account.avatarUrl}
					<img src={post.account.avatarUrl} alt="" />
				{:else}
					<span>{post.account.username.slice(0, 1).toUpperCase()}</span>
				{/if}
			</div>

			<div class="account">
				<div>
					<strong>{post.account.displayName ?? post.account.username}</strong>
					<span>@{post.account.username}</span>
				</div>
				<time datetime={post.createdAt}>{formatDate(post.createdAt)}</time>
			</div>
		</header>

		<p>{post.text}</p>

		<footer>
			<span>{post.likes ?? 0} いいね</span>
			<span>{post.comments ?? 0} コメント</span>
		</footer>

		{#if deleteError}
			<p class="delete-error">{deleteError}</p>
		{/if}

		<button class="delete-button" type="button" onclick={handleDelete} disabled={isDeleting}>
			{isDeleting ? '削除中...' : '削除'}
		</button>
	</div>
</article>

<style>
	.post {
		display: flex;
		height: 100%;
		overflow: hidden;
		flex-direction: column;
		border: 1px solid var(--border);
		border-radius: 8px;
		background: var(--surface);
	}

	.post-image {
		display: block;
		width: 100%;
		aspect-ratio: 1 / 1;
		object-fit: cover;
		background: var(--surface-muted);
	}

	.body {
		display: flex;
		flex: 1;
		flex-direction: column;
		min-width: 0;
		padding: 12px;
	}

	.avatar {
		width: 34px;
		height: 34px;
		flex: 0 0 auto;
		overflow: hidden;
		border-radius: 50%;
		background: var(--brand);
		color: #ffffff;
		font-weight: 800;
		display: grid;
		place-items: center;
	}

	.avatar img {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	header {
		display: flex;
		gap: 10px;
		align-items: center;
		margin-bottom: 10px;
	}

	.account {
		min-width: 0;
	}

	.account div {
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
		align-items: baseline;
	}

	strong {
		font-size: 15px;
		line-height: 1.2;
	}

	.account span,
	time,
	footer {
		color: var(--muted);
		font-size: 13px;
	}

	p {
		flex: 1;
		margin: 0 0 12px;
		line-height: 1.45;
		white-space: pre-wrap;
	}

	footer {
		display: flex;
		flex-wrap: wrap;
		gap: 8px 14px;
		margin-top: auto;
	}

	.delete-error {
		flex: 0;
		margin: 10px 0 0;
		color: var(--danger);
		font-size: 13px;
	}

	.delete-button {
		align-self: flex-start;
		margin-top: 10px;
		border: 1px solid var(--border);
		border-radius: 8px;
		background: var(--surface-muted);
		color: var(--danger);
		cursor: pointer;
		font: inherit;
		font-size: 13px;
		font-weight: 800;
		padding: 7px 10px;
	}

	.delete-button:hover {
		background: var(--surface-soft);
	}

	.delete-button:disabled {
		cursor: not-allowed;
		opacity: 0.7;
	}

	@media (max-width: 520px) {
		.avatar {
			width: 32px;
			height: 32px;
		}

		.body {
			padding: 10px;
		}

		time {
			display: block;
			margin-top: 2px;
		}
	}
</style>
