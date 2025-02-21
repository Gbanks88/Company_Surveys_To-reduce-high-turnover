import React, { useState } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  Select,
  Textarea,
  VStack,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
  useToast,
} from '@chakra-ui/react';

const RequirementForm = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    type: 'FUNCTIONAL',
    priority: 3,
    acceptance_criteria: '',
    stakeholders: '',
  });

  const toast = useToast();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/requirements/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          acceptance_criteria: formData.acceptance_criteria.split('\n'),
          stakeholders: formData.stakeholders.split(',').map(s => s.trim()),
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to create requirement');
      }

      toast({
        title: 'Requirement created.',
        description: "We've created your requirement for you.",
        status: 'success',
        duration: 9000,
        isClosable: true,
      });

      setFormData({
        title: '',
        description: '',
        type: 'FUNCTIONAL',
        priority: 3,
        acceptance_criteria: '',
        stakeholders: '',
      });

      if (onSubmit) {
        onSubmit();
      }
    } catch (error) {
      toast({
        title: 'Error creating requirement.',
        description: error.message,
        status: 'error',
        duration: 9000,
        isClosable: true,
      });
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <Box as="form" onSubmit={handleSubmit}>
      <VStack spacing={4}>
        <FormControl isRequired>
          <FormLabel>Title</FormLabel>
          <Input
            name="title"
            value={formData.title}
            onChange={handleChange}
            placeholder="Enter requirement title"
          />
        </FormControl>

        <FormControl isRequired>
          <FormLabel>Description</FormLabel>
          <Textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Enter detailed description"
          />
        </FormControl>

        <FormControl isRequired>
          <FormLabel>Type</FormLabel>
          <Select name="type" value={formData.type} onChange={handleChange}>
            <option value="FUNCTIONAL">Functional</option>
            <option value="NON_FUNCTIONAL">Non-Functional</option>
            <option value="BUSINESS">Business</option>
            <option value="TECHNICAL">Technical</option>
          </Select>
        </FormControl>

        <FormControl isRequired>
          <FormLabel>Priority (1-5)</FormLabel>
          <NumberInput
            name="priority"
            value={formData.priority}
            min={1}
            max={5}
            onChange={(value) => setFormData(prev => ({ ...prev, priority: parseInt(value) }))}
          >
            <NumberInputField />
            <NumberInputStepper>
              <NumberIncrementStepper />
              <NumberDecrementStepper />
            </NumberInputStepper>
          </NumberInput>
        </FormControl>

        <FormControl isRequired>
          <FormLabel>Acceptance Criteria (one per line)</FormLabel>
          <Textarea
            name="acceptance_criteria"
            value={formData.acceptance_criteria}
            onChange={handleChange}
            placeholder="Enter acceptance criteria"
          />
        </FormControl>

        <FormControl>
          <FormLabel>Stakeholders (comma-separated)</FormLabel>
          <Input
            name="stakeholders"
            value={formData.stakeholders}
            onChange={handleChange}
            placeholder="Enter stakeholders"
          />
        </FormControl>

        <Button
          mt={4}
          colorScheme="teal"
          type="submit"
        >
          Create Requirement
        </Button>
      </VStack>
    </Box>
  );
};

export default RequirementForm;
