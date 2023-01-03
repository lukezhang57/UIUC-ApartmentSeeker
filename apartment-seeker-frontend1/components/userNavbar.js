import { Box, Link, Text } from "@chakra-ui/react"
import NextLink from 'next/link'

const UserNavbar = () => {
  return (
    <Box 
      display="flex" 
      alignItems="center" 
      justifyContent="space-between" 
      mx={5} py={4}
      
    >
      <Box>
        <Text fontWeight="bold">ApartmentSeeker</Text>
      </Box>
      <Box>
        
        <NextLink href={'/login'} passHref>
          <Link pr={4} fontWeight="semibold">Login</Link>
        </NextLink>
      
      
        <NextLink href={'/signup'} passHref>
          <Link fontWeight="semibold">Signup</Link>
        </NextLink>
        
      </Box>

    </Box>
  )
}

export default UserNavbar