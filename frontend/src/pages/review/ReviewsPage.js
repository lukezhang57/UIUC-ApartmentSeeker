import React, { useEffect, useState } from 'react'
import Navbar from '../../components/Navbar'
import { 
  Box, Container, Select, 
   Text, Heading, Button,Flex,
    FormControl, VStack, Divider, 
    Modal, ModalOverlay,ModalContent,ModalHeader,ModalCloseButton,ModalBody,
    FormLabel,ModalFooter, useDisclosure, Input, Textarea, Grid, Center, useToast
} from '@chakra-ui/react'
import { SearchIcon, ExternalLinkIcon, Icon, StarIcon } from '@chakra-ui/icons'
import { MdCheckCircle, MdPerson, MdStop, MdThumbDown, MdThumbUp } from 'react-icons/md'
import StarRating from '../../components/StarRating'
import axios from 'axios'
import StarRatingView from '../../components/StarRatingView'
import { useLocation } from 'react-router'
import { Link } from 'react-router-dom'

const Reviews = () => {

  const [reviews, setReviews] = useState()

  const { isOpen, onOpen, onClose } = useDisclosure()

  const initialRef = React.useRef()
  const finalRef = React.useRef()
  const location = useLocation()
  const apartment_slug = location.pathname.split('/')[3]
  console.log('slug: ' + apartment_slug)

  // login message toast
  const toast = useToast()


  // get user here
  const user = JSON.parse(localStorage.getItem("user"));

  // for the current review being written
  const [reviewText, setReviewText] = useState()
  const [maintainenceRating, setMaintenanceRating] = useState()
  const [cleanlinessRating, setCleanlinessRating] = useState()
  const [overallRating, setOverallRating] = useState()

  const [likes, setLikes] = useState(0)
  const [dislikes, setDislikes] = useState(0)


  const handleClick = (type, name) => {
    const sendChange = async (type) => {
      try {
        if (type === 0) {
          setLikes(likes + 1)
          const res = await axios.post(`http://127.0.0.1:8000/api/like_review?user_name=${user.user_name}&review_user_name=${name}&apartment_slug=${apartment_slug}`)
          console.log('res: ' , res)
          getData()
          
        } else if (type === 1) {
          setDislikes(dislikes + 1)
          const res = await axios.post(`http://127.0.0.1:8000/api/dislike_review?user_name=${user.user_name}&review_user_name=${name}&apartment_slug=${apartment_slug}`)
          getData()
          
        }
        
      } catch (e) {
        console.log(e)
      }
    }
    if (user) {
      sendChange(type)
    } else {
      alert("You must be logged in to write a review!")
    }
    
  }

  // const handlePostReview = () => {
  //   const postReview = (type) => {
  //     try {
  //       const res = axios.post(`http://127.0.0.1:8000/api/post_review`)
  //     } catch (e) {
  //       console.log(e)
  //     }
  //   }
  //   postReview()
  // }

  const getData = async () => {
    console.log('trying to add stuff')
    try {
      const res = await axios.get(
        `http://127.0.0.1:8000/api/get_apartment_reviews?apartment_slug=${apartment_slug}`
      )
      console.log(res.data)
      setReviews(res.data)
    } catch (e) {
      console.log('error: ' + e)
    }
  }

  useEffect(() => {
    getData()
  },[])

  return (
    <>
      <Navbar />
      {reviews ? 
        (<Box mt={2}>
          <Container maxWidth="container.xl" bg="white" boxShadow="xl" borderWidth={1} borderColor="gray.200" py={4} px={4}>
            <Box>
              <Text fontSize="sm" color="gray.700">Viewing Reviews for</Text>
              <Heading size="xl">{apartment_slug}</Heading>
              <Button mt={4} mr={2} colorScheme="blue" size="sm" onClick={onOpen}>Write a Review</Button>
              <Link to={`/apartments/sublease/${apartment_slug}`}>
                <Button mt={4} colorScheme="pink" size="sm" >View Subleases</Button>
              </Link>
              
            </Box>
          </Container>

          <Container maxWidth="container.xl" shadow="lg" padding={0} mt={2}>
            <Flex gap={2}>
              <Box flex={3}  bg="white" width='full'  py={4} px={4} mt={2}>
                
                <Heading size="lg">Leave a Review</Heading>

                <FormControl mt={4}>
                  <FormLabel>Review</FormLabel>
                  <Textarea placeholder='Write your review here ...' onChange={(e) => {
                    setReviewText(e.target.value)
                  }} />
                </FormControl>
                <FormControl mt={4}>
                  <Text>Maintenance</Text>
                  <StarRating setRatingState={setMaintenanceRating} />
                </FormControl>
                <FormControl mt={4}>
                  <Text>Cleanliness</Text>
                  <StarRating setRatingState={setCleanlinessRating} />
                </FormControl>
                <FormControl mt={4}>
                  <Text>Overall</Text>
                  <StarRating setRatingState={setOverallRating} />
                </FormControl>
                <Button mt={6} size="md" colorScheme="teal" onClick={(e) => {
                  e.preventDefault()
                  if (user) {
                    try {
                      const res = axios.post(
                        `http://127.0.0.1:8000/api/post_review?apartmentSlug=${apartment_slug}&userName=${user.user_name}&reviewText=${reviewText}&maintainenceRating=${maintainenceRating}&overallRating=${overallRating}&cleanlinessRating=${cleanlinessRating}&quietnessRating=${3}&costRating=${2}`
                      )
                      console.log(res)
                      console.log('send successful')
                      window.location.reload()
                    } catch (e) {
                      console.log(e)
                    }
                  } else {
                    // show message that they need to sign up first
                    toast({
                      title: 'Please login to write a review.',
                      description: "Only logged in users can write a review.",
                      status: 'error',
                      duration: 9000,
                      isClosable: true,
                    })

                  }
                  
                  



              //     params={"userName":user_name, "reviewText": review_text, 
              //  "costRating":cost_rating,
              //  "overallRating": overall_rating,
              //  "maintainenceRating":maintainence_rating,
              // "quietnessRating": quietness_rating,
              // "cleanlinessRating":cleanliness_rating, "apartmentSlug":apartment_slug}
                }}>Submit Review</Button>
              </Box>

              <Box flex={2}  mt={2} px={4} bg="white" >
                

                <Box py={2}>
                  {
                    console.log(reviews)
                  }
                  {reviews.map((review, i) => (
                    <Box key={i}>
                      <Box my={3} >
                        <Box d="flex" flexDirection="column">
                          <Box d="flex">
                            <Icon as={MdPerson} w={10} h={10} />
                            <VStack spacing={0}>
                              <Box d="flex" alignItems="center">
                                {review.verified ? 
                                  <>
                                    <Icon as={MdCheckCircle} color="green.500" w={4} h={4} mr={1} />
                                    <Text fontSize="lg" fontWeight="bold">Verified Student</Text>
                                  </> :
                                  <>
                                    <Icon as={MdStop} color="red.500" w={4} h={4} mr={1} />
                                    <Text fontSize="lg" fontWeight="bold">{review.review_text.split(':')[0]}</Text>
                                  </>
                                }
                                
                              </Box>
                              <Box ml={1}>
                                <Text fontSize="xs" color="gray.700">Lived here 2018-2019</Text>
                              </Box>
                            </VStack>
                          </Box>

                          <Flex mt={2}>
                            <Text>Maintenance: </Text>
                            <StarRatingView rating={review.quietness_rating} />
                          </Flex>
                          <Flex mt={1}>
                            <Text>Cleanliness: </Text>
                            <StarRatingView rating={review.cleanliness_rating} />
                          </Flex>
                          
                          <Flex mt={1}>
                            <Text>Overall: </Text>
                            <StarRatingView rating={review.overall_rating} />
                          </Flex>
                          
                          <Box mt={2}>
                            <Text fontSize="xl">
                              {review.review_text.split(':')[1]}
                            </Text>
                          </Box>
                          <Box mt={4} d="flex" alignItems="center">
                            <Icon 
                              w={6}
                              h={6} 
                              as={MdThumbUp} 
                              cursor="pointer" 
                              onClick={(e) => {
                                handleClick(0, review.user.user_name)
                              }}
                            />
                            <Box w={1}/>
                            <Text mr={3}>{review.likes.length > likes ?  review.likes.length : likes}</Text>
                            <Icon  
                              w={6} 
                              h={6} 
                              as={MdThumbDown}  
                              cursor="pointer" 
                              onClick={(e) => {
                                handleClick(1, review.user.user_name)
                              }}
                            />
                            <Box w={1}/>
                            <Text>{review.dislikes.lenghth > dislikes ?  review.dislikes.length : dislikes}</Text>
                          </Box>
                        </Box>
                      </Box>
                      {i !== reviews.length - 1 && <Divider />}
                    </Box>
                  ))}
                </Box>
              </Box>
            </Flex>
          </Container>
        </Box>) : <div>Loading ...</div>}
      <Box h={200}></Box>

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
