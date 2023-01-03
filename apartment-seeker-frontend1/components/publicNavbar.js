import { Box, Link, Text } from "@chakra-ui/react"
import NextLink from 'next/link'

const PublicNavbar = () => {
  return (
    
    <Box 
      display="flex" 
      alignItems="center" 
      justifyContent="space-between" 
      px={5} py={4}
      bg="gray.900"
      borderBottom={1}
      borderColor="gray.200"
      borderStyle="solid"
      
    >
      <Box>
        <Text fontWeight="semibold" color="white">ApartmentSeeker</Text>
      </Box>
      <Box>
        
        <NextLink href={'/login'} passHref>
          <Link pr={4} color="whiteAlpha.900" >Login</Link>
        </NextLink>
      
      
        <NextLink href={'/signup'} passHref>
          <Link color="whiteAlpha.900">Signup</Link>
        </NextLink>
        
      </Box>

    </Box>
  )
}

export default PublicNavbar