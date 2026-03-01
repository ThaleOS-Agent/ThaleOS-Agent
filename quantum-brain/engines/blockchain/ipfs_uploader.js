// ============================================
// ThaléOS IPFS Uploader
// ============================================
import { create } from 'ipfs-http-client';

const client = create({ url: 'https://ipfs.infura.io:5001' });

export async function uploadToIPFS(file) {
    const result = await client.add(file);
    return `ipfs://${result.path}`;
}
