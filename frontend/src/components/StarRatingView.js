import React, { useState } from 'react'
import { Box, HStack } from '@chakra-ui/react'
import { StarIcon } from '@chakra-ui/icons'

const StarRatingView = ({ rating }) => {
  
  return (
    <Box>
      <HStack
      >
        <Box>
          <StarIcon 
            boxSize={4} 
            color={rating > 0 ? '#FDCC0D' : '#ffffff'} 
          />
        </Box>
        <Box>
          <StarIcon 
            boxSize={4} 
            color={rating > 1 ? '#FDCC0D' : '#ffffff'} 
          />
        </Box>
        <Box>
          <StarIcon 
            boxSize={4} color={rating > 2 ? '#FDCC0D' : '#ffffff'} 
          />
        </Box>
        <Box>
          <StarIcon 
            boxSize={4}
            color={rating > 3 ? '#FDCC0D' : '#ffffff'} 
          />
        </Box>
        <Box>
          <StarIcon 
            boxSize={4} 
            color={rating > 4 ? '#FDCC0D' : '#ffffff'}  
          />
        </Box>
        
        
        
        
      </HStack>
    </Box>
  )
}

export default StarRatingView