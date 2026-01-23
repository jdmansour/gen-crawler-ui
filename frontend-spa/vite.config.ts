/// <reference types="vitest/config" />
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';
import svgr from 'vite-plugin-svgr';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { storybookTest } from '@storybook/addon-vitest/vitest-plugin';

// Derive __dirname in ESM
const __dirname = path.dirname(fileURLToPath(import.meta.url));

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const baseConfig = {
    plugins: [react(), svgr()],
    test: {
      projects: [
        {
          extends: './vitest.config.ts' as any,
          plugins: [
            storybookTest({
              configDir: path.join(__dirname, '.storybook'),
            }),
          ],
          test: {
            name: 'storybook',
            browser: {
              enabled: true,
              headless: true,
              provider: 'playwright',
              instances: [{ browser: 'chromium' }],
            },
            setupFiles: ['.storybook/vitest.setup.ts'],
          },
        },
      ],
    },
  };

  if (mode === 'library') {
    // Library build configuration
    return {
      ...baseConfig,
      define: {
        'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV)
      },
      css: {
        modules: {
          // Ensure CSS modules work in library mode
          localsConvention: 'camelCase',
          // Keep original class names instead of hashing
          generateScopedName: "[local]",
        }
      },
      build: {
        lib: {
          entry: resolve(__dirname, 'src/elements/wlo-gen-crawler.tsx'),
          name: 'WloComponents',
          fileName: 'index',
          formats: ['es']
        },
        rollupOptions: {
          // nothing is external, we don't use react in wlo
          external: [
          ],
          output: {
            globals: {
              react: 'React',
              'react-dom': 'ReactDOM',
              'react-router-dom': 'ReactRouterDOM',
              'react/jsx-runtime': 'react/jsx-runtime'
            },
            // Ensure CSS is included in the build
            assetFileNames: (assetInfo) => {
              if (assetInfo.name && assetInfo.name.endsWith('.css')) {
                return 'style.css';
              }
              return assetInfo.name || '';
            }
          }
        },
        cssCodeSplit: false,
        sourcemap: true,
        minify: false // Für besseres Debugging
      }
    };
  }
  
  // Default development configuration (für Storybook und Dev-Server)
  return {
    ...baseConfig,
    server: {
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          secure: false,
        },
      },
    },
    build: {
      rollupOptions: {
        input: {
          main: resolve(__dirname, 'index.html'),
          test_component: resolve(__dirname, 'test_component.html'),
        },
      },
    },
  };
});
