import React, { useState } from 'react';
import {
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Badge,
  Box,
  Input,
  Select,
  IconButton,
  useToast,
  Tooltip,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
} from '@chakra-ui/react';
import { ViewIcon } from '@chakra-ui/icons';

const RequirementsTable = ({ requirements, onUpdate }) => {
  const [filter, setFilter] = useState({
    title: '',
    type: '',
    priority: '',
    status: '',
  });
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [selectedRequirement, setSelectedRequirement] = useState(null);
  const toast = useToast();

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilter(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const filteredRequirements = requirements.filter(req => {
    return (
      (!filter.title || req.title.toLowerCase().includes(filter.title.toLowerCase())) &&
      (!filter.type || req.type === filter.type) &&
      (!filter.priority || req.priority === parseInt(filter.priority)) &&
      (!filter.status || req.status === filter.status)
    );
  });

  const handleViewDetails = (requirement) => {
    setSelectedRequirement(requirement);
    onOpen();
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 1: return 'red';
      case 2: return 'orange';
      case 3: return 'yellow';
      case 4: return 'green';
      case 5: return 'blue';
      default: return 'gray';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'DRAFT': return 'gray';
      case 'REVIEW': return 'yellow';
      case 'APPROVED': return 'green';
      case 'REJECTED': return 'red';
      default: return 'gray';
    }
  };

  return (
    <Box>
      <Box mb={4} display="flex" gap={4}>
        <Input
          placeholder="Filter by title"
          name="title"
          value={filter.title}
          onChange={handleFilterChange}
        />
        <Select
          placeholder="Filter by type"
          name="type"
          value={filter.type}
          onChange={handleFilterChange}
        >
          <option value="FUNCTIONAL">Functional</option>
          <option value="NON_FUNCTIONAL">Non-Functional</option>
          <option value="BUSINESS">Business</option>
          <option value="TECHNICAL">Technical</option>
        </Select>
        <Select
          placeholder="Filter by priority"
          name="priority"
          value={filter.priority}
          onChange={handleFilterChange}
        >
          {[1, 2, 3, 4, 5].map(p => (
            <option key={p} value={p}>{p}</option>
          ))}
        </Select>
        <Select
          placeholder="Filter by status"
          name="status"
          value={filter.status}
          onChange={handleFilterChange}
        >
          <option value="DRAFT">Draft</option>
          <option value="REVIEW">Review</option>
          <option value="APPROVED">Approved</option>
          <option value="REJECTED">Rejected</option>
        </Select>
      </Box>

      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>ID</Th>
            <Th>Title</Th>
            <Th>Type</Th>
            <Th>Priority</Th>
            <Th>Status</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>
        <Tbody>
          {filteredRequirements.map((req) => (
            <Tr key={req._id}>
              <Td>{req._id}</Td>
              <Td>{req.title}</Td>
              <Td>
                <Badge>{req.type}</Badge>
              </Td>
              <Td>
                <Badge colorScheme={getPriorityColor(req.priority)}>
                  P{req.priority}
                </Badge>
              </Td>
              <Td>
                <Badge colorScheme={getStatusColor(req.status)}>
                  {req.status}
                </Badge>
              </Td>
              <Td>
                <Tooltip label="View Details">
                  <IconButton
                    icon={<ViewIcon />}
                    onClick={() => handleViewDetails(req)}
                    aria-label="View details"
                  />
                </Tooltip>
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>

      <Modal isOpen={isOpen} onClose={onClose} size="xl">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Requirement Details</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            {selectedRequirement && (
              <Box>
                <Table variant="simple">
                  <Tbody>
                    <Tr>
                      <Th>Title</Th>
                      <Td>{selectedRequirement.title}</Td>
                    </Tr>
                    <Tr>
                      <Th>Description</Th>
                      <Td>{selectedRequirement.description}</Td>
                    </Tr>
                    <Tr>
                      <Th>Type</Th>
                      <Td>
                        <Badge>{selectedRequirement.type}</Badge>
                      </Td>
                    </Tr>
                    <Tr>
                      <Th>Priority</Th>
                      <Td>
                        <Badge colorScheme={getPriorityColor(selectedRequirement.priority)}>
                          P{selectedRequirement.priority}
                        </Badge>
                      </Td>
                    </Tr>
                    <Tr>
                      <Th>Status</Th>
                      <Td>
                        <Badge colorScheme={getStatusColor(selectedRequirement.status)}>
                          {selectedRequirement.status}
                        </Badge>
                      </Td>
                    </Tr>
                    <Tr>
                      <Th>Acceptance Criteria</Th>
                      <Td>
                        <ul>
                          {selectedRequirement.acceptance_criteria.map((criterion, index) => (
                            <li key={index}>{criterion}</li>
                          ))}
                        </ul>
                      </Td>
                    </Tr>
                    <Tr>
                      <Th>Stakeholders</Th>
                      <Td>
                        {selectedRequirement.stakeholders.join(', ')}
                      </Td>
                    </Tr>
                  </Tbody>
                </Table>
              </Box>
            )}
          </ModalBody>
        </ModalContent>
      </Modal>
    </Box>
  );
};

export default RequirementsTable;
