<script lang="ts">
	const posts = [
		{
			title: 'Neon City Dream',
			author: 'Luna Sketch',
			type: 'Digital Painting',
			likes: '1.2k',
			comments: '189',
			image: 'https://picsum.photos/seed/neon-city/900/520',
		},
		{
			title: 'Forest Spirit Study',
			author: 'Kai Mori',
			type: 'Concept Art',
			likes: '984',
			comments: '73',
			image: 'https://picsum.photos/seed/forest/900/520',
		},
		{
			title: 'Starship Reflections',
			author: 'Ari Vance',
			type: '3D Render',
			likes: '860',
			comments: '54',
			image: 'https://picsum.photos/seed/starship/900/520',
		},
		{
			title: 'Mythic Portrait',
			author: 'Nova Rae',
			type: 'Illustration',
			likes: '1.5k',
			comments: '216',
			image: 'https://picsum.photos/seed/portrait/900/520',
		},
	];
</script>

<section class="feed-grid">
	{#each posts as post}
		<article class="art-card">
			<div class="art-thumbnail">
				<img src={post.image} alt={post.title} loading="lazy" />
			</div>
			<div class="card-body">
				<div class="card-meta">
					<span>{post.type}</span>
					<span>•</span>
					<span>{post.likes} likes</span>
				</div>
				<h3>{post.title}</h3>
				<div class="card-footer">
					<div>
						<strong>{post.author}</strong>
						<span>{post.comments} comments</span>
					</div>
					<button class="view-btn">View</button>
				</div>
			</div>
		</article>
	{/each}
</section>

<style>
	.feed-grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 22px;
	}

	.art-card {
		background: #ffffff;
		border: 1px solid #e8e4ff;
		border-radius: 32px;
		overflow: hidden;
		display: flex;
		flex-direction: column;
		box-shadow: 0 24px 50px rgba(95, 78, 193, 0.08);
	}

	.art-thumbnail {
		height: 220px;
		background: linear-gradient(135deg, #fde8ff 0%, #f5f3ff 100%);
		overflow: hidden;
	}

	.art-thumbnail img {
		width: 100%;
		height: 100%;
		object-fit: cover;
		display: block;
	}

	.card-body {
		padding: 24px;
		display: flex;
		flex-direction: column;
		gap: 18px;
	}

	.card-meta {
		display: flex;
		align-items: center;
		gap: 10px;
		color: #8a7fb8;
		font-size: 0.92rem;
	}

	.card-meta span:first-child {
		font-weight: 700;
		color: #6d5caf;
	}

	.card-body h3 {
		margin: 0;
		font-size: 1.25rem;
		color: #2d2644;
	}

	.card-footer {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 14px;
	}

	.card-footer strong {
		display: block;
		font-size: 0.98rem;
		color: #2d2644;
	}

	.card-footer span {
		color: #7b6e9c;
		font-size: 0.9rem;
	}

	.view-btn {
		padding: 12px 18px;
		border: none;
		border-radius: 18px;
		background: #f6efff;
		color: #554a8e;
		cursor: pointer;
		font-family: 'Sora', 'Poppins', sans-serif;
		font-weight: 600;
		letter-spacing: 0.02em;
	}

	@media (max-width: 900px) {
		.feed-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
