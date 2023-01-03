import { 
  Box, FormControl, 
  Input, Heading, Stack,
  FormLabel, Flex, Button, Grid
} from '@chakra-ui/react'



const Signup = () => {
  

  return (
    <Flex justify="center" align="center" minHeight="100vh" bg="gray.50">
      <Stack spacing="10">
        
        <Stack align="center">
          <Heading fontWeight="semibold">Create an account</Heading>
        </Stack>
        <Box bg="white" py="10" px="7" rounded="lg" boxShadow="lg">
          <Stack>
            <Grid templateColumns='repeat(2, 1fr)' gap={3}>
              <FormControl>
                <FormLabel htmlFor="firstName">First name</FormLabel>
                <Input id="firstName" type="text" />
              </FormControl>
              <FormControl>
                <FormLabel htmlFor="lastName">Last name</FormLabel>
                <Input id="lastName" type="text" />
              </FormControl>
            </Grid>
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

export default Signup