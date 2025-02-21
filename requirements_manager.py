#!/usr/bin/env python3
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
from bson import ObjectId
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.database import Database
from dotenv import load_dotenv

class RequirementType(Enum):
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    BUSINESS = "business"
    TECHNICAL = "technical"
    SECURITY = "security"
    PERFORMANCE = "performance"
    USABILITY = "usability"

class RequirementStatus(Enum):
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    IMPLEMENTED = "implemented"
    VERIFIED = "verified"
    REJECTED = "rejected"

class UseCaseStatus(Enum):
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    IMPLEMENTED = "implemented"
    TESTED = "tested"

class RequirementsManager:
    """Requirements and Use Case Management System."""
    
    def __init__(self):
        """Initialize the requirements manager."""
        load_dotenv()
        
        # MongoDB connection
        self.mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.db_name = os.getenv('MONGODB_DB', 'survey_analytics')
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.db_name]
        
        # Collections
        self.requirements = self.db['requirements']
        self.use_cases = self.db['use_cases']
        self.stakeholders = self.db['stakeholders']
        self.relationships = self.db['requirement_relationships']
        self.history = self.db['requirement_history']
        
        # Create indexes
        self._setup_indexes()
    
    def _setup_indexes(self):
        """Set up MongoDB indexes."""
        # Requirements indexes
        self.requirements.create_index([("req_id", ASCENDING)], unique=True)
        self.requirements.create_index([("status", ASCENDING)])
        self.requirements.create_index([("type", ASCENDING)])
        self.requirements.create_index([("priority", DESCENDING)])
        
        # Use cases indexes
        self.use_cases.create_index([("uc_id", ASCENDING)], unique=True)
        self.use_cases.create_index([("status", ASCENDING)])
        self.use_cases.create_index([("priority", DESCENDING)])
        
        # Relationships index
        self.relationships.create_index([
            ("source_id", ASCENDING),
            ("target_id", ASCENDING)
        ])
    
    def create_requirement(self, data: Dict[str, Any]) -> str:
        """Create a new requirement."""
        try:
            requirement = {
                "req_id": f"REQ-{self._get_next_sequence('requirements')}",
                "title": data["title"],
                "description": data["description"],
                "type": data["type"].value,
                "status": RequirementStatus.DRAFT.value,
                "priority": data.get("priority", 3),  # 1 (highest) to 5 (lowest)
                "stakeholders": data.get("stakeholders", []),
                "acceptance_criteria": data.get("acceptance_criteria", []),
                "dependencies": data.get("dependencies", []),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "created_by": data.get("created_by", "system"),
                "metadata": data.get("metadata", {})
            }
            
            result = self.requirements.insert_one(requirement)
            
            # Record history
            self._record_history("requirement", str(result.inserted_id), "created", requirement)
            
            return str(result.inserted_id)
            
        except Exception as e:
            print(f"Error creating requirement: {str(e)}")
            raise
    
    def create_use_case(self, data: Dict[str, Any]) -> str:
        """Create a new use case."""
        try:
            use_case = {
                "uc_id": f"UC-{self._get_next_sequence('use_cases')}",
                "title": data["title"],
                "description": data["description"],
                "actor": data["actor"],
                "preconditions": data.get("preconditions", []),
                "postconditions": data.get("postconditions", []),
                "main_flow": data["main_flow"],
                "alternative_flows": data.get("alternative_flows", []),
                "status": UseCaseStatus.DRAFT.value,
                "priority": data.get("priority", 3),
                "requirements": data.get("requirements", []),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "created_by": data.get("created_by", "system"),
                "metadata": data.get("metadata", {})
            }
            
            result = self.use_cases.insert_one(use_case)
            
            # Link to requirements
            for req_id in use_case["requirements"]:
                self.create_relationship(
                    str(result.inserted_id),
                    req_id,
                    "implements"
                )
            
            return str(result.inserted_id)
            
        except Exception as e:
            print(f"Error creating use case: {str(e)}")
            raise
    
    def update_requirement_status(self, req_id: str, status: RequirementStatus) -> bool:
        """Update requirement status."""
        try:
            result = self.requirements.update_one(
                {"_id": ObjectId(req_id)},
                {
                    "$set": {
                        "status": status.value,
                        "updated_at": datetime.now().isoformat()
                    }
                }
            )
            
            if result.modified_count > 0:
                self._record_history(
                    "requirement",
                    req_id,
                    "status_updated",
                    {"status": status.value}
                )
                return True
            return False
            
        except Exception as e:
            print(f"Error updating requirement status: {str(e)}")
            raise
    
    def create_relationship(self, source_id: str, target_id: str, 
                          relationship_type: str) -> str:
        """Create a relationship between requirements/use cases."""
        try:
            relationship = {
                "source_id": source_id,
                "target_id": target_id,
                "type": relationship_type,
                "created_at": datetime.now().isoformat()
            }
            
            result = self.relationships.insert_one(relationship)
            return str(result.inserted_id)
            
        except Exception as e:
            print(f"Error creating relationship: {str(e)}")
            raise
    
    def get_requirement_trace(self, req_id: str) -> Dict[str, Any]:
        """Get requirement traceability matrix."""
        try:
            # Get requirement details
            requirement = self.requirements.find_one({"_id": ObjectId(req_id)})
            if not requirement:
                raise ValueError(f"Requirement {req_id} not found")
            
            # Get related use cases
            related_use_cases = list(self.use_cases.find({
                "requirements": req_id
            }))
            
            # Get dependencies
            dependencies = list(self.relationships.find({
                "$or": [
                    {"source_id": req_id},
                    {"target_id": req_id}
                ]
            }))
            
            return {
                "requirement": requirement,
                "use_cases": related_use_cases,
                "dependencies": dependencies
            }
            
        except Exception as e:
            print(f"Error getting requirement trace: {str(e)}")
            raise
    
    def _get_next_sequence(self, name: str) -> int:
        """Get next sequence number for IDs."""
        sequence_collection = self.db['sequences']
        sequence = sequence_collection.find_one_and_update(
            {"_id": name},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=True
        )
        return sequence["seq"]
    
    def _record_history(self, item_type: str, item_id: str, 
                       action: str, data: Dict[str, Any]):
        """Record history of changes."""
        try:
            history_entry = {
                "item_type": item_type,
                "item_id": item_id,
                "action": action,
                "data": data,
                "timestamp": datetime.now().isoformat()
            }
            
            self.history.insert_one(history_entry)
            
        except Exception as e:
            print(f"Error recording history: {str(e)}")
    
    def close(self):
        """Close MongoDB connection."""
        self.client.close()

def test_requirements_manager():
    """Test the requirements management system."""
    try:
        manager = RequirementsManager()
        
        # Create a requirement
        req_data = {
            "title": "User Authentication",
            "description": "System must provide secure user authentication",
            "type": RequirementType.SECURITY,
            "priority": 1,
            "acceptance_criteria": [
                "Support username/password authentication",
                "Implement password complexity rules",
                "Lock accounts after failed attempts"
            ]
        }
        
        req_id = manager.create_requirement(req_data)
        print(f"✓ Created requirement: {req_id}")
        
        # Create a use case
        uc_data = {
            "title": "User Login",
            "description": "Allow user to log into the system",
            "actor": "End User",
            "preconditions": ["User has valid account"],
            "postconditions": ["User is authenticated"],
            "main_flow": [
                "1. User navigates to login page",
                "2. User enters credentials",
                "3. System validates credentials",
                "4. System grants access"
            ],
            "requirements": [req_id]
        }
        
        uc_id = manager.create_use_case(uc_data)
        print(f"✓ Created use case: {uc_id}")
        
        # Get traceability
        trace = manager.get_requirement_trace(req_id)
        print(f"✓ Generated traceability matrix")
        print(f"  Related use cases: {len(trace['use_cases'])}")
        
        manager.close()
        return True
        
    except Exception as e:
        print(f"✗ Error testing requirements manager: {str(e)}")
        return False

if __name__ == "__main__":
    test_requirements_manager()
