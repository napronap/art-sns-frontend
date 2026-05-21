<script lang="ts">
	import { onDestroy } from 'svelte';
	import { createPost, type Post } from '$lib/api';

	let { onCreated }: { onCreated?: (post: Post) => void } = $props();

	let isOpen = $state(false);
	let text = $state('');
	let image = $state<File | null>(null);
	let previewUrl = $state<string | null>(null);
	let isSubmitting = $state(false);
	let error = $state('');

	function openComposer() {
		error = '';
		isOpen = true;
	}

	function closeComposer() {
		if (isSubmitting) {
			return;
		}

		isOpen = false;
		clearForm();
	}

	function setImage(file: File | null) {
		if (previewUrl) {
			URL.revokeObjectURL(previewUrl);
		}

		image = file;
		previewUrl = file ? URL.createObjectURL(file) : null;
	}

	function handleImageChange(event: Event) {
		const input = event.currentTarget as HTMLInputElement;
		setImage(input.files?.[0] ?? null);
	}

	function clearForm() {
		text = '';
		setImage(null);
		error = '';
	}

	async function submitPost(event: SubmitEvent) {
		event.preventDefault();

		if (!image) {
			error = '画像を選択してください。';
			return;
		}

		if (!text.trim()) {
			error = '画像に添える本文を入力してください。';
			return;
		}

		isSubmitting = true;
		error = '';

		try {
			const post = await createPost({ text: text.trim(), image });
			onCreated?.(post);
			isOpen = false;
			clearForm();
		} catch {
			error = '投稿をアップロードできませんでした。';
		} finally {
			isSubmitting = false;
		}
	}

	onDestroy(() => {
		if (previewUrl) {
			URL.revokeObjectURL(previewUrl);
		}
	});
</script>

<button class="upload-button" type="button" onclick={openComposer}>アップロード</button>

{#if isOpen}
	<div class="backdrop">
		<section class="composer" aria-label="投稿をアップロード">
			<header>
				<h2>投稿をアップロード</h2>
				<button class="close-button" type="button" onclick={closeComposer} aria-label="閉じる"
					>×</button
				>
			</header>

			<form onsubmit={submitPost}>
				<label>
					本文
					<textarea bind:value={text} maxlength="280" rows="4" placeholder="何を共有しますか？"
					></textarea>
				</label>

				<label>
					画像
					<input type="file" accept="image/*" onchange={handleImageChange} />
				</label>

				{#if previewUrl}
					<img class="preview" src={previewUrl} alt="プレビュー" />
				{/if}

				{#if error}
					<p class="error">{error}</p>
				{/if}

				<div class="actions">
					<button type="button" class="secondary" onclick={closeComposer}>キャンセル</button>
					<button type="submit" disabled={isSubmitting}>
						{isSubmitting ? 'アップロード中...' : '投稿する'}
					</button>
				</div>
			</form>
		</section>
	</div>
{/if}

<style>
	.upload-button,
	form button {
		border: 0;
		border-radius: 8px;
		background: var(--brand);
		color: #ffffff;
		cursor: pointer;
		font-weight: 800;
	}

	.upload-button {
		padding: 10px 16px;
	}

	.upload-button:hover,
	form button:hover {
		background: var(--brand-hover);
	}

	.backdrop {
		position: fixed;
		inset: 0;
		z-index: 50;
		display: grid;
		place-items: center;
		padding: 18px;
		background: var(--overlay);
	}

	.composer {
		width: min(520px, 100%);
		border-radius: 8px;
		background: var(--surface);
		box-shadow: var(--shadow);
	}

	header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 12px;
		padding: 14px 16px;
		border-bottom: 1px solid var(--border);
	}

	h2 {
		margin: 0;
		font-size: 18px;
	}

	.close-button {
		width: 32px;
		height: 32px;
		border: 1px solid var(--border);
		border-radius: 8px;
		background: var(--surface);
		color: var(--muted-strong);
		cursor: pointer;
		font-size: 18px;
		line-height: 1;
	}

	form {
		display: grid;
		gap: 14px;
		padding: 16px;
	}

	label {
		display: grid;
		gap: 6px;
		font-size: 14px;
		font-weight: 800;
		color: var(--muted-strong);
	}

	textarea,
	input {
		width: 100%;
		border: 1px solid var(--border-strong);
		border-radius: 8px;
		background: var(--surface);
		color: var(--text);
		padding: 10px;
		font: inherit;
	}

	textarea:focus,
	input:focus {
		outline: 2px solid var(--focus);
		border-color: var(--brand);
	}

	.preview {
		width: 100%;
		max-height: 280px;
		object-fit: cover;
		border-radius: 8px;
		border: 1px solid var(--border);
	}

	.error {
		margin: 0;
		color: var(--danger);
		font-size: 14px;
	}

	.actions {
		display: flex;
		justify-content: flex-end;
		gap: 10px;
	}

	form button {
		padding: 10px 14px;
	}

	form button:disabled {
		cursor: not-allowed;
		opacity: 0.7;
	}

	.secondary {
		background: var(--surface-muted);
		color: var(--muted-strong);
	}

	.secondary:hover {
		background: var(--surface-soft);
	}
</style>
