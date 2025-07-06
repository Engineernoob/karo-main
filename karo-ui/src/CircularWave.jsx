import { Box, usePrefersReducedMotion } from "@chakra-ui/react";
import { keyframes } from "@emotion/react";

export default function CircularWave({ isActive }) {
  const prefersReducedMotion = usePrefersReducedMotion();

  // Define the pulsing ring keyframes using Emotion
  const pulse = keyframes`
    0%   { transform: scale(0); opacity: 0.8; }
    50%  { transform: scale(1); opacity: 0.4; }
    100% { transform: scale(1.5); opacity: 0; }
  `;

  const animation = prefersReducedMotion
    ? undefined
    : `${pulse} 2s infinite ease-out`;

  if (!isActive) return null;

  return (
    <Box
      position="fixed"
      inset={0}
      display="flex"
      alignItems="center"
      justifyContent="center"
      pointerEvents="none"
      zIndex={9999}
    >
      {/* Render three staggered pulse rings */}
      {[0, 1, 2].map((i) => (
        <Box
          key={i}
          position="absolute"
          w="192px"
          h="192px"
          border="2px solid"
          borderColor="whiteAlpha.800"
          borderRadius="full"
          animation={animation}
          animationDelay={`${i * 0.6}s`}
        />
      ))}

      {/* Inner static core circle */}
      <Box
        position="relative"
        w="48px"
        h="48px"
        bg="white"
        borderRadius="full"
        boxShadow="0 0 10px whiteAlpha.800"
      />
    </Box>
  );
}