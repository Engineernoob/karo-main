import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { ChakraProvider, extendTheme } from "@chakra-ui/react";

// Optional: customize the Chakra theme
const theme = extendTheme({
  styles: {
    global: {
      body: { bg: "gray.800", color: "grey", margin: 0, padding: 0 },
    },
  },
});

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ChakraProvider theme={theme}>
      <App />
    </ChakraProvider>
  </React.StrictMode>
);
