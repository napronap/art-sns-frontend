import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

const apiTarget = 'http://127.0.0.1:8010';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		proxy: {
			'/api': apiTarget,
			'/uploads': apiTarget
		}
	}
});
