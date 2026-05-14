<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div>
	this is a menu methinks lmao
</div>

{@render children()}

<div>
	layout some other stuffs and sht
</div>