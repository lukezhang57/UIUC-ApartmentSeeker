import { 
  Box, FormControl, 
  Input, Heading, Stack,
  FormLabel, Flex, Button, Grid
} from '@chakra-ui/react'


const Login = () => {
  return (
    <Flex justify="center" align="center" minHeight="100vh" bg="gray.50">
      <Stack spacing="10">
        
        <Stack align="center">
          <Heading fontWeight="semibold">Log in to ApartmentSeeker</Heading>
        </Stack>
        <Box bg="white" py="10" px="7" rounded="lg" boxShadow="lg">
          <Stack>
            <FormControl>
              <FormLabel htmlFor="email">Email</FormLabel>
              <Input id="email" type="email" />
            </FormControl>
            <FormControl>
              <FormLabel htmlFor="password">Password</FormLabel>
              <Input id="password" type="password" />
            </FormControl>
            
          </Stack>
          <Button 
            color="white" 
            bg="blue.500" 
            mt="5" 
            w="100%"
            _hover={{ bg:"blue.400" }}
          >
            Login
          </Button>
        </Box>
      </Stack>
    </Flex>
  )
}

export default Login