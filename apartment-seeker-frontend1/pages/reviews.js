import React, { useState } from 'react'
import Navbar from '../components/publicNavbar'
import { 
  Box, Container, Select, 
   Text, Heading, Button,Flex,
    FormControl, VStack, Divider, 
    Modal, ModalOverlay,ModalContent,ModalHeader,ModalCloseButton,ModalBody,
    FormLabel,ModalFooter, useDisclosure, Input, Textarea
} from '@chakra-ui/react'
import { SearchIcon, ExternalLinkIcon, Icon, StarIcon } from '@chakra-ui/icons'
import { MdWarning, MdCheckCircle, MdPerson, MdOutlineWarning, MdThumbDownOffAlt, MdThumbUpOffAlt } from 'react-icons/md'
import StarRating from '../components/StarRating'

const Reviews = () => {

  const [reviews, setReviews] = useState([
    {
      verified: true,
      apartment: 'Bankier Apartments',
      text: 'Lived here 2 years ago. Great amenities, but rent is expensive. Wouldrecommend if money is not problem!',
      date: '5/12/2018',
      _id: '1'
    },
    {
      verified: false,
      apartment: 'Bankier Apartments',
      text: 'Terrible apartment. Neighbors are always playing music and I could never concentrate on my studies. Find some other apartment. Everything else but this one.',
      date: '5/12/2018',
      _id: '2'
    },
    {
      verified: true,
      apartment: 'Bankier Apartments',
      text: 'Lived here 2 years ago. Great amenities, but rent is expensive. Wouldrecommend if money is not problem!',
      date: '5/12/2018',
      _id: '3'
    }
  ])

  const { isOpen, onOpen, onClose } = useDisclosure()

  const initialRef = React.useRef()
  const finalRef = React.useRef()

  return (
    <>
      <Navbar />
      <Box mt={2}>
        <Container maxWidth="container.xl" bg="white" boxShadow="xl" borderWidth={1} borderColor="gray.200" py={4} px={4}>
          <Box>
            <Text fontSize="sm" color="gray.700">Viewing Reviews for</Text>
            <Heading size="xl">Bankier Apartments</Heading>
            <Button mt={4} mr={2} colorScheme="blue" size="sm" onClick={onOpen}>Write a Review</Button>
            <Button mt={4} colorScheme="pink" size="sm" >View Subleases</Button>
          </Box>
        </Container>

        <Container maxWidth="container.xl" bg="white" borderWidth={1} borderColor="gray.200" py={4} px={4} mt={2}>
          
          <Heading size="lg">Leave a Review</Heading>

          <FormControl mt={4}>
            <FormLabel>Review</FormLabel>
            <Textarea placeholder='Write your review here ...' />
          </FormControl>
          <FormControl mt={4}>
            <Text>Privacy</Text>
            <StarRating />
          </FormControl>
          <FormControl mt={4}>
            <Text>Cleanliness</Text>
            <StarRating />
          </FormControl>
          <FormControl mt={4}>
            <Text>Amenities</Text>
            <StarRating />
          </FormControl>
          
          <Button mt={6} size="md" colorScheme="teal">Submit Review</Button>
          
          
        </Container>


        <Container mt={2} maxW="container.xl" bg="white" borderWidth={1} borderColor="gray.200">
          <Flex gap={2} mt={4} mb={4}>
            <Box>
              <FormControl>
                <Select size="sm" width={200}>
                  <option value='newest'>Newest reviews first</option>
                  <option value='oldest'>Oldest reviews first</option>
                </Select>
              </FormControl>
            </Box>
            <Box>
              <FormControl>
                <Select size="sm" width={200}>
                  <option value='positive'>Positive reviews first</option>
                  <option value='negative'>Negative reviews first</option>
                </Select>
              </FormControl>
            </Box>

          </Flex>

          <Box py={2}>
            {reviews.map((review, i) => (
              <>
                <Box my={3}>
                  <Box d="flex" flexDirection="column">
                    <Box d="flex">
                      <Icon as={MdPerson} w={10} h={10} />
                      <VStack spacing={0}>
                        <Box d="flex" alignItems="center">
                          {review.verified ? 
                            <>
                              <Icon as={MdCheckCircle} color="green.500" w={4} h={4} mr={1} />
                              <Text fontSize="sm" fontWeight="bold">Verified Student</Text>
                            </> :
                            <>
                              <Icon as={MdOutlineWarning} color="red.500" w={4} h={4} mr={1} />
                              <Text fontSize="sm" fontWeight="bold">Unverified User</Text>
                            </>
                          }
                          
                        </Box>
                        <Box ml={1}>
                          <Text fontSize="xs" color="gray.700">Lived here 2018-2019</Text>
                        </Box>
                      </VStack>
                    </Box>
                    <Box>
                      <Text></Text>
                    </Box>
                    <Box mt={2}>
                      <Text fontSize="lg">
                        {review.text}
                      </Text>
                    </Box>
                    <Box mt={4}>
                        <Icon as={MdThumbDownOffAlt} />
                        <Icon as={MdThumbUpOffAlt} />
                    </Box>
                  </Box>
                </Box>
                {i !== reviews.length - 1 && <Divider />}
              </>
            ))}
          </Box>
        </Container>
      </Box>

      {/* Modal */}
      <Modal
        initialFocusRef={initialRef}
        finalFocusRef={finalRef}
        isOpen={isOpen}
        onClose={onClose}
        isCentered
      >
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Please leave your review</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <FormControl>
              <FormLabel>Privacy</FormLabel>
              <StarRating />
            </FormControl>

            <FormControl mt={4}>
              <FormLabel>Comfort</FormLabel>
              <StarRating />
            </FormControl>

            <FormControl mt={4}>
              <FormLabel>Cleanliness</FormLabel>
              <Textarea placeholder='Write your review here ...' />
            </FormControl>
          </ModalBody>

          <ModalFooter>
            <Button colorScheme='blue' mr={3}>
              Save
            </Button>
            <Button onClick={onClose}>Cancel</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>

    </>
  )
}

export default Reviews