import { defineConfig } from 'vite';
import { viteSingleFile } from 'vite-plugin-singlefile';
import path from 'path';

// The production build is a single self-contained index.html: vite-plugin-singlefile inlines
// all JS/CSS into the HTML, and a very high assetsInlineLimit forces every sprite SVG to be
// embedded as a data: URI rather than emitted as a separate file. The result runs by
// double-clicking the file in any browser on any OS, offline, with no install or dev server.
export default defineConfig({
  base: './',
  plugins: [viteSingleFile()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  build: {
    target: 'esnext',
    assetsInlineLimit: 100 * 1024 * 1024,
  },
});
