import React from 'react'
import Navbar from '../components/publicNavbar'
import { 
  Box, Container, Select, NumberInput, NumberInputField, 
  NumberInputStepper, NumberIncrementStepper, NumberDecrementStepper,
   Text, Heading, Tag, Image, Button, Badge,
   Grid, FormControl, GridItem, HStack, Link, FormLabel, VStack 
} from '@chakra-ui/react'
import { SearchIcon, ExternalLinkIcon, Icon, StarIcon } from '@chakra-ui/icons'
import { MdWarning } from 'react-icons/md'

const University = () => {
  return (
    <>
      <Navbar />
      <Box pt={2} mt={2}>
        <Container maxWidth="container.xl" >
          <Box 
            display="flex" 
            alignItem="center" 
            py={4}
            bg="white"
            boxShadow="md"
            px={6}
          >
            <Box>
              <Image w={150} h={150} borderRadius="full" alt="school-image" src="https://burnham310.com/wp-content/uploads/2020/09/UIUC-Student-Union-1.jpg" />
            </Box>
            <Box ml={5}>
              <Text color="gray.600" fontWeight="semibold" fontSize="lg">Apartments located at</Text>
              <Heading size="lg">
                Univeristy of Illinois at Urbana Champaign
              </Heading>
              <Box display="flex" alignItems="center" mt={2}>
                <Box color="blue.600" textTransform="uppercase" fontWeight="bold">
                  Urbana, Champaign
                </Box>
                
                <Link isExternal ml={2} color="gray.700" >
                  Visit School Website <ExternalLinkIcon mx='2px' />
                </Link>
                               
              </Box>
              <HStack mt={1}>
                <Text fontSize="sm" color="gray.700">44,087 students</Text>
                <Text  fontSize="sm" color="gray.700">Dorms required for <strong>Freshmen</strong></Text>
              </HStack>
              <HStack spacing={2} mt={2}>
                <Badge colorScheme="green">Public Institution</Badge>
                <Badge colorScheme="blue">Large Student Body</Badge>
                <Badge colorScheme="red">State School</Badge>
              </HStack>
            </Box>

          </Box>
          <Grid>
          </Grid>
        </Container>

        <Container maxWidth="container.xl" mt={2}>
          <Grid templateColumns='repeat(6, 1fr)' gap={3}>
            <GridItem colSpan={1}>
              <Box bg="white" boxShadow="md" px={3} py={4}>
                <VStack alignItems="left">
                  <Heading size="xs" mb={2}>
                    Apply Filters
                  </Heading>
                  <FormControl>
                    <FormLabel fontSize="sm">Price Range</FormLabel>
                    <Select size="xs">
                      <option value='499OrBelow'>$499 and Below</option>
                      <option value='500To999'>$500 - $999</option>
                    </Select>
                  </FormControl>
                  <FormControl>
                    <FormLabel fontSize="sm">Price Range</FormLabel>
                    <Select size="xs">
                      <option value='499OrBelow'>$499 and Below</option>
                      <option value='500To999'>$500 - $999</option>
                    </Select>
                  </FormControl>
                  <FormControl>
                    <FormLabel fontSize="sm">Price Range</FormLabel>
                    <Select size="xs">
                      <option value='499OrBelow'>$499 and Below</option>
                      <option value='500To999'>$500 - $999</option>
                    </Select>
                  </FormControl>
                  <FormControl>
                    <FormLabel fontSize="sm">Minimum Overall Rating</FormLabel>
                    <NumberInput size="xs" defaultValue={3} min={1} max={5}>
                      <NumberInputField />
                      <NumberInputStepper>
                        <NumberIncrementStepper />
                        <NumberDecrementStepper />
                      </NumberInputStepper>
                    </NumberInput>
                  </FormControl>

                </VStack>
              </Box>
            </GridItem>
            <GridItem colSpan={5}>
              {/* For the reviews */}
              <Grid templateColumns='repeat(4, 1fr)' gap={2}>
                <Box width="100%" bg="white" boxShadow="md">
                  {/* MAKE SURE TO USE NEXT.JS IMAGES LATER */}
                  <Image width="100%" objectFit="cover" height={250} alt="ucla" src="https://www.bankierapartments.com/uploads/images/homepage-image-01.jpg" />
                  <Box px={3} py={3}>
                    <Text textTransform="uppercase" fontWeight="bold" fontSize="xs">
                      406 E Green St
                    </Text>
                    <Heading size="md">
                      Bankier Apartments
                    </Heading>
                    <Box mt={1} d="flex">
                      <HStack spacing={1}>
                        <StarIcon boxSize={3} color="yellow.300" />
                        <StarIcon boxSize={3} color="yellow.300" />
                        <StarIcon boxSize={3} color="yellow.300" />
                        <StarIcon boxSize={3} color="yellow.300" />
                        <StarIcon boxSize={3} color="gray.300" />
                      </HStack>
                      <Text ml={2} color="gray.500" fontSize="xs">Average 4.5/5</Text>
                    </Box>
                    <Text color="gray.600" fontSize="xs" mt={1}>
                      17 total reviews
                    </Text>
                    <Button 
                      mt="2" 
                      size="xs" 
                      width="100%" 
                      color="white" 
                      bg="teal.500"
                      _hover={{ bg:"teal.400" }}
                    >
                      Browse Reviews
                    </Button>
                  </Box>
                </Box>
                <Box width="100%" bg="white" boxShadow="md">
                  {/* MAKE SURE TO USE NEXT.JS IMAGES LATER */}
                  <Image width="100%" objectFit="cover" height={250} alt="ucla" src="https://www.thedean.com/campustown/wp-content/uploads/2021/03/0000_9444.jpg" />
                  <Box px={3} py={3}>
                    <Text textTransform="uppercase" fontWeight="bold" fontSize="xs">
                      708 S 6th St
                    </Text>
                    <Heading size="md">
                      The Dean Campustown
                    </Heading>
                    <Box mt={1} d="flex">
                      <HStack spacing={1}>
                        <StarIcon boxSize={3} color="yellow.300" />
                        <StarIcon boxSize={3} color="yellow.300" />
                        <StarIcon boxSize={3} color="yellow.300" />
                        <StarIcon boxSize={3} color="yellow.300" />
                        <StarIcon boxSize={3} color="gray.300" />
                      </HStack>
                      <Text ml={2} color="gray.500" fontSize="xs">Average 4.5/5</Text>
                    </Box>
                    <Text color="gray.600" fontSize="xs" mt={1}>
                      20 total reviews
                    </Text>
                    <Button 
                      mt="2" 
                      size="xs" 
                      width="100%" 
                      color="white" 
                      bg="teal.500"
                      _hover={{ bg:"teal.400" }}
                    >
                      Browse Reviews
                    </Button>
                  </Box>
                </Box>
                <Box width="100%" bg="white" boxShadow="md">
                  {/* MAKE SURE TO USE NEXT.JS IMAGES LATER */}
                  <Image width="100%" objectFit="cover" height={250} alt="ucla" src="https://www.opus-group.com/Media/ProjectImages/University-of-Illinois-Luxury-Student-Housing-Development_5934_1000x667.jpg?v=637122198200000000" />
                  <Box px={3} py={3}>
                    <Text textTransform="uppercase" fontWeight="bold" fontSize="xs">
                      707 S 4th St, Champaign
                    </Text>
                    <Heading size="md">
                      Seven07
                    </Heading>
                    <Box mt={1} d="flex">
                      <HStack spacing={1}>
                        <StarIcon boxSize={3} color="yellow.300" />
                        <StarIcon boxSize={3} color="yellow.300" />
                        <StarIcon boxSize={3} color="yellow.300" />
                        <StarIcon boxSize={3} color="yellow.300" />
                        <StarIcon boxSize={3} color="gray.300" />
                      </HStack>
                      <Text ml={2} color="gray.500" fontSize="xs">Average 4.5/5</Text>
                    </Box>
                    <Text color="gray.600" fontSize="xs" mt={1}>
                      20 total reviews
                    </Text>
                    <Button 
                      mt="2" 
                      size="xs" 
                      width="100%" 
                      color="white" 
                      bg="teal.500"
                      _hover={{ bg:"teal.400" }}
                    >
                      Browse Reviews
                    </Button>
                  </Box>
                </Box>
                <Box width="100%" bg="white" boxShadow="md">
                  {/* MAKE SURE TO USE NEXT.JS IMAGES LATER */}
                  <Image width="100%" objectFit="cover" height={250} alt="ucla" src="https://www.opus-group.com/Media/ProjectImages/University-of-Illinois-Luxury-Student-Housing-Development_5934_1000x667.jpg?v=637122198200000000" />
                  <Box px={3} py={3}>
                    <Text textTransform="uppercase" fontWeight="bold" fontSize="xs">
                      707 S 4th St, Champaign
                    </Text>
                    <Heading size="md">
                      Seven07
                    </Heading>
                    <Box mt={1} d="flex">
                      <HStack spacing={1}>
                        <StarIcon boxSize={3} color="yellow.300" />
                        <StarIcon boxSize={3} color="yellow.300" />
                        <StarIcon boxSize={3} color="yellow.300" />
                        <StarIcon boxSize={3} color="yellow.300" />
                        <StarIcon boxSize={3} color="gray.300" />
                      </HStack>
                      <Text ml={2} color="gray.500" fontSize="xs">Average 4.5/5</Text>
                    </Box>
                    
                      
                      <Text color="gray.600" fontSize="xs">
                        20 total reviews
                      </Text>
                    
                    <Button 
                      mt="2" 
                      size="xs" 
                      width="100%" 
                      color="white" 
                      bg="teal.500"
                      _hover={{ bg:"teal.400" }}
                    >
                      Browse Reviews
                    </Button>
                  </Box>
                </Box>
              </Grid>

              
              
              



              
            </GridItem>

          </Grid>
        </Container>
      </Box>
    </>
  )
}

export default University