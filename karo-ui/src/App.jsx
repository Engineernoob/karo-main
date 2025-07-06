import { useState } from "react";
import { Button, Box } from "@chakra-ui/react";
import CircularWave from "./CircularWave";

export default function App() {
  const [listening, setListening] = useState(false);
  return (
    <Box
      minH="100vh"
      display="flex"
      flexDir="column"
      alignItems="center"
      justifyContent="center"
      bg="gray.800"
      color="white"
    >
      <Button colorScheme="blue" mb={6} onClick={() => setListening(v => !v)}>
        {listening ? "Stop Listening" : "Activate Karo"}
      </Button>
      <CircularWave isActive={listening} />
    </Box>
  );
}
