const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const path = require("path");
const webpack = require("webpack");

const mode = process.env.NODE_ENV || "development";
const prod = mode === "production";

module.exports = {
  entry: {
    bundle: ["./src/main.js"],
  },
  resolve: {
    alias: {
      svelte: path.resolve("node_modules", "svelte"),
    },
    extensions: [".mjs", ".js", ".svelte"],
    mainFields: ["svelte", "browser", "module", "main"],
  },
  output: {
    path: __dirname + "/public",
    filename: "[name].js",
    chunkFilename: "[name].[id].js",
  },
  module: {
    rules: [
      {
        test: /\.svelte$/,
        use: {
          loader: "svelte-loader",
          options: {
            emitCss: true,
            hotReload: true,
          },
        },
      },
      {
        test: /\.css$/,
        use: [
          /**
           * MiniCssExtractPlugin doesn't support HMR.
           * For developing, use 'style-loader' instead.
           * */
          prod ? MiniCssExtractPlugin.loader : "style-loader",
          "css-loader",
        ],
      },
    ],
  },
  mode,
  plugins: [
    new MiniCssExtractPlugin({
      filename: "[name].css",
    }),
    // replace CHECKERS_API_URL environment variable in build.
    new webpack.EnvironmentPlugin({
      HEXPLODE_BACKEND: "localhost:8000",
    }),
  ],
  devtool: prod ? false : "source-map",
  devServer: {
    contentBase: path.join(__dirname, "public"),
    compress: true,
    port: 8080,
    host: process.env.WEBPACK_DEV_SERVER_HOST || "localhost",
  },
};
