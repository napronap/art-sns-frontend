export type Account = {
	id: string;
	username: string;
	email: string;
	displayName?: string;
	bio?: string;
	avatarUrl?: string;
	createdAt?: string;
};

export type Post = {
	id: string;
	text: string;
	imageUrl: string;
	createdAt: string;
	account: Account;
	likes?: number;
	comments?: number;
};

export type PostsPage = {
	posts: Post[];
	nextCursor: string | null;
	hasMore: boolean;
};

const API_BASE = '/api';
const PAGE_SIZE = 5;

const demoAccount: Account = {
	id: 'sakura_art',
	username: 'sakura_art',
	displayName: 'さくら',
	email: 'sakura@example.jp',
	bio: '画像SNSのCRUDを試すためのデモアカウントです。',
	createdAt: '2026-05-01T12:00:00.000Z'
};

const demoAccounts: Account[] = [
	demoAccount,
	{
		id: 'yuki_photo',
		username: 'yuki_photo',
		displayName: 'ゆき',
		email: 'yuki@example.jp'
	},
	{
		id: 'aoi_sketch',
		username: 'aoi_sketch',
		displayName: 'あおい',
		email: 'aoi@example.jp'
	}
];

const demoPosts: Post[] = [
	{
		id: 'demo-1',
		text: '新しいシリーズの最初のラフです。',
		imageUrl: 'https://picsum.photos/seed/art-sns-1/900/620',
		createdAt: '2026-05-21T08:20:00.000Z',
		account: demoAccount,
		likes: 12,
		comments: 2
	},
	{
		id: 'demo-2',
		text: '構図の練習用に、質感と光を試しています。',
		imageUrl: 'https://picsum.photos/seed/art-sns-2/900/620',
		createdAt: '2026-05-21T07:30:00.000Z',
		account: demoAccounts[1],
		likes: 8,
		comments: 1
	},
	{
		id: 'demo-3',
		text: '参考用に撮った写真です。',
		imageUrl: 'https://picsum.photos/seed/art-sns-3/900/620',
		createdAt: '2026-05-20T21:10:00.000Z',
		account: demoAccounts[2],
		likes: 21,
		comments: 4
	},
	{
		id: 'demo-4',
		text: '明るめのカラーパレットを試しています。',
		imageUrl: 'https://picsum.photos/seed/art-sns-4/900/620',
		createdAt: '2026-05-20T18:45:00.000Z',
		account: demoAccount,
		likes: 5,
		comments: 0
	},
	{
		id: 'demo-5',
		text: '制作途中のディテールです。',
		imageUrl: 'https://picsum.photos/seed/art-sns-5/900/620',
		createdAt: '2026-05-20T16:00:00.000Z',
		account: demoAccounts[1],
		likes: 17,
		comments: 3
	},
	{
		id: 'demo-6',
		text: 'ポートフォリオに載せる前の完成版です。',
		imageUrl: 'https://picsum.photos/seed/art-sns-6/900/620',
		createdAt: '2026-05-19T12:25:00.000Z',
		account: demoAccount,
		likes: 31,
		comments: 6
	},
	{
		id: 'demo-7',
		text: '縦長の構図テストです。',
		imageUrl: 'https://picsum.photos/seed/art-sns-7/900/620',
		createdAt: '2026-05-18T22:05:00.000Z',
		account: demoAccounts[2],
		likes: 9,
		comments: 1
	}
];

async function getJson<T>(path: string): Promise<T> {
	const response = await fetch(path);

	if (!response.ok) {
		throw new Error(`Request failed: ${response.status}`);
	}

	return (await response.json()) as T;
}

function normalizePostsPage(data: unknown): PostsPage {
	if (Array.isArray(data)) {
		return {
			posts: data as Post[],
			nextCursor: null,
			hasMore: false
		};
	}

	const page = data as Partial<PostsPage> & { data?: Post[] };
	const posts = page.posts ?? page.data ?? [];

	return {
		posts,
		nextCursor: page.nextCursor ?? null,
		hasMore: page.hasMore ?? posts.length === PAGE_SIZE
	};
}

function demoPostsPage(cursor: string | null): PostsPage {
	const start = Number(cursor ?? 0) || 0;
	const posts = demoPosts.slice(start, start + PAGE_SIZE);
	const nextIndex = start + posts.length;

	return {
		posts,
		nextCursor: nextIndex < demoPosts.length ? String(nextIndex) : null,
		hasMore: nextIndex < demoPosts.length
	};
}

export async function fetchPosts(cursor: string | null = null): Promise<PostsPage> {
	const params = new URLSearchParams({ limit: String(PAGE_SIZE) });

	if (cursor) {
		params.set('cursor', cursor);
	}

	try {
		const data = await getJson<unknown>(`${API_BASE}/posts?${params.toString()}`);
		return normalizePostsPage(data);
	} catch {
		return demoPostsPage(cursor);
	}
}

export async function fetchCurrentAccount(): Promise<Account> {
	try {
		return await getJson<Account>(`${API_BASE}/me`);
	} catch {
		return demoAccount;
	}
}

export async function fetchProfilePosts(): Promise<Post[]> {
	try {
		const data = await getJson<unknown>(`${API_BASE}/me/posts`);

		if (Array.isArray(data)) {
			return data as Post[];
		}

		const page = data as Partial<PostsPage> & { data?: Post[] };
		return page.posts ?? page.data ?? [];
	} catch {
		return demoPosts.filter((post) => post.account.id === demoAccount.id);
	}
}

export async function createPost(input: { text: string; image: File }): Promise<Post> {
	const formData = new FormData();
	formData.append('text', input.text);
	formData.append('image', input.image);

	try {
		const response = await fetch(`${API_BASE}/posts`, {
			method: 'POST',
			body: formData
		});

		if (!response.ok) {
			throw new Error(`Request failed: ${response.status}`);
		}

		const data = (await response.json()) as Post | { post: Post };
		return 'post' in data ? data.post : data;
	} catch {
		const id =
			typeof crypto !== 'undefined' && 'randomUUID' in crypto
				? crypto.randomUUID()
				: String(Date.now());

		return {
			id,
			text: input.text,
			imageUrl: URL.createObjectURL(input.image),
			createdAt: new Date().toISOString(),
			account: demoAccount,
			likes: 0,
			comments: 0
		};
	}
}
