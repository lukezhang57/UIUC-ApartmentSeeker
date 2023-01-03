import React, { useState } from 'react'
import { Box, HStack } from '@chakra-ui/react'
import { StarIcon } from '@chakra-ui/icons'

const StarRating = ({ setRatingState }) => {
  const [rating, setRating] = useState(0)
  const [storedRating, setStoredRating] = useState(0)
  
  const handleMouseEnter = (rating) => {
    setStoredRating(rating)
    setRating(rating)
    setRatingState(rating)
  }

  const handleMouseLeave = () => {
    
    setRating(storedRating)
  }
  return (
    <Box>
      
      <HStack
        
      >
        <Box>
          <StarIcon 
            boxSize={8} 
            color={rating > 0 ? '#FDCC0D' : 'yellow.100'} 
            onClick={() => setRating(1)} 
            onMouseEnter={() => handleMouseEnter(1)}
            onMouseLeave={handleMouseLeave}
          />
        </Box>
        <Box>
          <StarIcon 
            boxSize={8} 
            color={rating > 1 ? '#FDCC0D' : 'yellow.100'} 
            onClick={() => setRating(2)} 
            onMouseEnter={() => handleMouseEnter(2)}
            onMouseLeave={handleMouseLeave} 
          />
        </Box>
        <Box>
          <StarIcon 
            boxSize={8} color={rating > 2 ? '#FDCC0D' : 'yellow.100'} 
            onClick={() => setRating(3)} 
            onMouseEnter={() => handleMouseEnter(3)}
            onMouseLeave={handleMouseLeave} 
          />
        </Box>
        <Box>
          <StarIcon 
            boxSize={8}
            color={rating > 3 ? '#FDCC0D' : 'yellow.100'} 
            onClick={() => setRating(4)} 
            onMouseEnter={() => handleMouseEnter(4)}
            onMouseLeave={handleMouseLeave}
          />
        </Box>
        <Box>
          <StarIcon boxSize={8} color={rating > 4 ? '#FDCC0D' : 'yellow.100'}  onClick={() => setRating(5)} onMouseEnter={() => handleMouseEnter(5)}
            onMouseLeave={handleMouseLeave}/>
        </Box>
        
        
        
        
      </HStack>
    </Box>
  )
}

export default StarRating