import { 
  Box, FormControl, 
  Input, Heading, Stack,
  FormLabel, Flex, Button, Grid, 
  Alert, AlertIcon, AlertTitle,
  Text
} from '@chakra-ui/react'
import Navbar from '../../components/Navbar'
import { useEffect, useState } from 'react'
import axios from 'axios';
import { useNavigate } from 'react-router';
import { Helmet } from 'react-helmet'

const Login = () => {

  const [username, getUsername] = useState("");

  const [password, getPassword] = useState("");

  const [error, setError] = useState(false);
  let navigate = useNavigate()


  const handleLogin = async () => {
    try {
      const user = {username, password};
      const response = await axios.get(`http://localhost:8000/api/sign_in?userName=${username}&password=${password}`);
      console.log(response.data);
      localStorage.setItem("user", JSON.stringify(response.data));

      navigate("/")
    } catch (error) {
      setError(true);
    } 
  }


  return (
    <>
      <Navbar/>
      <Flex justify="center" align="center" minHeight="100vh" bg="gray.50">
        <Helmet>
          <title>Log In | ApartmentSeeker</title>
        </Helmet>
        <Stack spacing="10">
          
          <Stack align="center">
            <Heading fontWeight="semibold">Log in to ApartmentSeeker</Heading>
          </Stack>
          <Box bg="white" py="10" px="7" rounded="lg" boxShadow="lg">
            <Stack>
              <FormControl>
                <FormLabel htmlFor="email">Username</FormLabel>
                <Input id="userName" type="userName" onChange={event => getUsername(event.currentTarget.value)}/>
              </FormControl>
              <FormControl>
                <FormLabel htmlFor="password">Password</FormLabel>
                <Input id="password" type="password" onChange={event => getPassword(event.currentTarget.value)}/>
              </FormControl>

              {error ? <Text color="red">User does not exist</Text> : <></>}

            </Stack>
            <Button 
              color="white" 
              bg="blue.500" 
              mt="5" 
              w="100%"
              _hover={{ bg:"blue.400" }}
              onClick={handleLogin}
            >
              Login
            </Button>
          </Box>
        </Stack>
      </Flex>
    </>
  )
}


export default Login