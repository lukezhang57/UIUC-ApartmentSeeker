import React, { useEffect, useState } from 'react'
import Navbar from '../components/Navbar'
import { 
  Box, 
  Container, 
  Text, Heading, 
  Image, Button, 
  Grid, FormControl, 
  Input
} from '@chakra-ui/react'
import { Link, Outlet } from 'react-router-dom'
import universitiesTmp from '../tmpData/universities'
import axios from 'axios'

const Home = () => {

  const [unis, setUnis] = useState()

  useEffect(() => {
    const getData = async () => {
      try {
        const res = await axios.get(
          `http://localhost:8000/api/universities/`
        )
        console.log(res.data)
        setUnis(res.data)
      } catch (e) {
        console.log('error', e)
      }
      
      
    }
    getData()
  },[])
  return (
    <div>
      <Navbar />

      <Box bg="gray.50" shadow="sm">
        <Container maxWidth="container.xl" py={20} >
          <Heading size="2xl">Welcome to ApartmentSeeker</Heading>
          <Text mt={4} fontSize="lg">Search for your school, browse apartments, and find subleases.</Text>
        </Container>
      </Box>
      <Container maxWidth="container.xl" mt={12}>
        <Box>
          <Heading>Browse Universities</Heading>
          <Grid templateColumns="repeat(6, 1fr)" gap={5} mt={2}>
            {unis?.map((uni, key) => (
              <Box width="100%" align="left" key={uni.id}>
                <Image width="100%" borderRadius="lg" alt="ucla" src={uni.img_url} />
                <Heading size="md" mt={2}>
                  {uni.name}
                </Heading>
                {/* <Text color="gray.600" fontSize="xs" mt={1}>
                  5 Apartments, 24 Reviews
                </Text> */}
                <Link to={`/university/${uni.university_slug}`}>
                  <Button
                    mt="2" 
                    size="sm" 
                    width="100%" 
                    color="white" 
                    bg="blue.500"
                    _hover={{ bg:"blue.400" }}
                  >
                    Browse Apartments
                  </Button>
                </Link>
              </Box>
              ))
            } 
          </Grid>
        </Box>
      </Container>
      <Box h={40}> </Box>
      <Outlet />
    </div>
  )
}

export default Home