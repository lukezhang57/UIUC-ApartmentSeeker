import React from 'react'
import Navbar from '../components/publicNavbar'
import { Box, Container, Text, Heading, Image, Button, Grid, FormControl, Input } from '@chakra-ui/react'
import { SearchIcon } from '@chakra-ui/icons'

const Home = () => {
  return (
    <>
      <Navbar />
      <Box>
        <Container maxWidth="container.xl">
          <Box>
            <Grid templateColumns="repeat(4, 1fr)" gap={5}>
              <Box width="100%" align="left">
                {/* MAKE SURE TO USE NEXT.JS IMAGES LATER */}
                <Image width="100%" borderRadius="lg" alt="ucla" src="https://s3.amazonaws.com/cms.ipressroom.com/173/files/20198/5d72b4772cfac209ff04c634_Royce+Quad/Royce+Quad_hero.jpg" />
                <Box mt="2" color="blue.600" textTransform="uppercase" fontWeight="bold">
                  Los Angeles, CA
                </Box>
                <Heading size="sm">
                  University of California, LA
                </Heading>
                <Text color="gray.600" fontSize="xs" mt={1}>
                  5 Apartments, 24 Reviews
                </Text>
                <Button
                  mt="2" 
                  size="xs" 
                  width="100%" 
                  color="white" 
                  bg="blue.500"
                  _hover={{ bg:"blue.400" }}
                >
                  Browse Apartments
                </Button>
              </Box>
              <Box width="100%">
                {/* MAKE SURE TO USE NEXT.JS IMAGES LATER */}
                <Image width="100%" borderRadius="lg" alt="ucla" src="https://burnham310.com/wp-content/uploads/2020/09/UIUC-Student-Union-1.jpg" />
                <Box mt="2" color="blue.600" textTransform="uppercase" fontWeight="bold">
                  Urbana, Champaign
                </Box>
                <Heading size="sm">
                  University of Illinois at Urbana Champaign
                </Heading>
                <Text color="gray.600" fontSize="xs" mt={1}>
                  5 Apartments, 24 Reviews
                </Text>
                <Button 
                  mt="2" 
                  size="xs" 
                  width="100%" 
                  color="white" 
                  bg="blue.500"
                  _hover={{ bg:"blue.400" }}
                >
                  Browse Apartments
                </Button>
              </Box>
              <Box width="100%">
                {/* MAKE SURE TO USE NEXT.JS IMAGES LATER */}
                <Image width="100%" borderRadius="lg" alt="ucla" src="https://s3.amazonaws.com/cms.ipressroom.com/173/files/20198/5d72b4772cfac209ff04c634_Royce+Quad/Royce+Quad_hero.jpg" />
                <Box mt="2" color="blue.600" textTransform="uppercase" fontWeight="bold">
                  Los Angeles, CA
                </Box>
                <Heading size="sm">
                  University of California, LA
                </Heading>
                <Text color="gray.600" fontSize="xs" mt={1}>
                  5 Apartments, 24 Reviews
                </Text>
                <Button 
                  mt="2" 
                  size="xs" 
                  width="100%" 
                  color="white" 
                  bg="blue.500"
                  _hover={{ bg:"blue.400" }}
                >
                  Browse Apartments
                </Button>
              </Box>
            </Grid>
          </Box>
        </Container>

        <Container maxW="container.xl" mt={10}>
          <Grid templateColumns="repeat(2, 1fr)" gap={3}>
            <Box>
              <Heading fontWeight="bold">
                Search a university to get started
              </Heading>
              <FormControl mt={4}>
                <Box position="relative">
                  <Input 
                    placeholder="Type &#8220;University of Michigan&#8220;" 
                    paddingLeft="7"
                  />
                  <Box position="absolute" top={2} left={2} fontSize="md">
                    <SearchIcon  />
                  </Box>
                </Box>
                <Button mt={2} 
                  bg="red.400" 
                  color="white" 
                  fontWeight="bold" 
                  width="100%"
                  _hover={{ bg:"red.300" }}
                >Search</Button>
              </FormControl>
              
            </Box>
          </Grid>
        </Container>
      </Box>
    </>
  )
}

export default Home