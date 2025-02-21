import React, { useState, useEffect } from 'react';
import {
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Box,
  Heading,
  Badge,
  Text,
  Tooltip,
  useColorModeValue,
} from '@chakra-ui/react';

const TraceabilityMatrix = ({ requirements, useCases }) => {
  const [matrix, setMatrix] = useState([]);
  const bgColor = useColorModeValue('gray.50', 'gray.700');
  const cellColor = useColorModeValue('green.100', 'green.700');

  useEffect(() => {
    generateMatrix();
  }, [requirements, useCases]);

  const generateMatrix = () => {
    const matrixData = requirements.map(req => {
      const row = {
        requirement: req,
        coverage: useCases.map(uc => ({
          useCase: uc,
          covered: uc.requirements.includes(req._id),
        })),
      };

      // Calculate coverage metrics
      row.totalCoverage = row.coverage.filter(c => c.covered).length;
      row.coveragePercentage = (row.totalCoverage / useCases.length) * 100;

      return row;
    });

    setMatrix(matrixData);
  };

  const getCoverageColor = (percentage) => {
    if (percentage >= 80) return 'green';
    if (percentage >= 50) return 'yellow';
    return 'red';
  };

  return (
    <Box overflowX="auto">
      <Heading size="md" mb={4}>Requirements Traceability Matrix</Heading>
      
      <Table variant="simple" size="sm">
        <Thead>
          <Tr bg={bgColor}>
            <Th>Requirement ID</Th>
            <Th>Title</Th>
            <Th>Priority</Th>
            {useCases.map(uc => (
              <Th key={uc._id} isNumeric>
                <Tooltip label={uc.title}>
                  <Text>UC-{uc._id.slice(-4)}</Text>
                </Tooltip>
              </Th>
            ))}
            <Th isNumeric>Coverage</Th>
          </Tr>
        </Thead>
        <Tbody>
          {matrix.map(row => (
            <Tr key={row.requirement._id}>
              <Td>REQ-{row.requirement._id.slice(-4)}</Td>
              <Td>
                <Tooltip label={row.requirement.description}>
                  <Text>{row.requirement.title}</Text>
                </Tooltip>
              </Td>
              <Td>
                <Badge>P{row.requirement.priority}</Badge>
              </Td>
              {row.coverage.map((cell, idx) => (
                <Td
                  key={`${row.requirement._id}-${idx}`}
                  bg={cell.covered ? cellColor : 'transparent'}
                  textAlign="center"
                >
                  {cell.covered ? '✓' : '-'}
                </Td>
              ))}
              <Td isNumeric>
                <Badge
                  colorScheme={getCoverageColor(row.coveragePercentage)}
                >
                  {Math.round(row.coveragePercentage)}%
                </Badge>
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>

      <Box mt={4}>
        <Heading size="sm" mb={2}>Coverage Summary</Heading>
        {matrix.map(row => (
          <Text key={row.requirement._id} fontSize="sm">
            {row.requirement.title}: {row.totalCoverage} use cases (
            <Badge
              colorScheme={getCoverageColor(row.coveragePercentage)}
            >
              {Math.round(row.coveragePercentage)}%
            </Badge>
            )
          </Text>
        ))}
      </Box>
    </Box>
  );
};

export default TraceabilityMatrix;
