import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  build: {
    rolldownOptions: {
      output: {
        codeSplitting: {
          groups: [
            { name: "antd", test: /node_modules[\\/](antd|@ant-design|@rc-component|rc-[^\\/]+)[\\/]/, priority: 3, maxSize: 400_000 },
            { name: "refine", test: /node_modules[\\/](@refinedev|@tanstack)[\\/]/, priority: 2, maxSize: 400_000 },
            { name: "vendor", test: /node_modules[\\/]/, priority: 1, maxSize: 400_000 },
          ],
        },
      },
    },
  },
});
