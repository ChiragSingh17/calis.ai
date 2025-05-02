
const admin = {
    "id": 1,
    "email": "admin@example.com",
    "password": "123"
};



const employees = [
    {
        "id": 1,
        "firstName": "Arjun",
        "email": "e@e.com",
        "password": "123",
        "tasks": [
            {
                "active": true,
                "newTask": false,
                "completed": false,
                "failed": false,
                "title": "Fix Bug #123",
                "description": "Resolve the issue causing crashes on the login page.",
                "date": "2025-02-01",
                "category": "Development"
            },
            {
                "active": false,
                "newTask": true,
                "completed": false,
                "failed": false,
                "title": "Team Meeting",
                "description": "Participate in the weekly team meeting to discuss project updates.",
                "date": "2025-02-03",
                "category": "Management"
            },
            {
                "active": false,
                "newTask": false,
                "completed": true,
                "failed": false,
                "title": "Update Documentation",
                "description": "Add the latest API changes to the documentation.",
                "date": "2025-01-28",
                "category": "Documentation"
            }
        ],
        "taskStats": { "active": 2, "newTask": 1, "completed": 1, "failed": 0 }
    },
    {
        "id": 2,
        "firstName": "Ravi",
        "email": "employee2@example.com",
        "password": "123",
        "tasks": [
            {
                "active": false,
                "newTask": true,
                "completed": false,
                "failed": false,
                "title": "Design Mockups",
                "description": "Create mockups for the new dashboard UI.",
                "date": "2025-02-05",
                "category": "Design"
            },
            {
                "active": true,
                "newTask": false,
                "completed": false,
                "failed": false,
                "title": "Fix Performance Issue",
                "description": "Optimize the database queries for faster load times.",
                "date": "2025-02-02",
                "category": "Development"
            }
        ],
        "taskStats": { "active": 1, "newTask": 1, "completed": 0, "failed": 0 }
    },
    {
        "id": 3,
        "firstName": "Priya",
        "email": "employee3@example.com",
        "password": "123",
        "tasks": [
            {
                "active": true,
                "newTask": true,
                "completed": false,
                "failed": false,
                "title": "Client Presentation",
                "description": "Prepare slides for the upcoming client pitch.",
                "date": "2025-01-30",
                "category": "Sales"
            },
            {
                "active": false,
                "newTask": false,
                "completed": true,
                "failed": false,
                "title": "Deploy Backend Service",
                "description": "Push the new microservice to production.",
                "date": "2025-01-27",
                "category": "Development"
            },
            {
                "active": false,
                "newTask": false,
                "completed": false,
                "failed": true,
                "title": "Bug Fix Sprint",
                "description": "Resolve critical bugs reported by QA.",
                "date": "2025-01-25",
                "category": "Testing"
            }
        ],
        "taskStats": { "active": 1, "newTask": 1, "completed": 1, "failed": 1 }
    },
    {
        "id": 4,
        "firstName": "Neha",
        "email": "employee4@example.com",
        "password": "123",
        "tasks": [
            {
                "active": true,
                "newTask": true,
                "completed": false,
                "failed": false,
                "title": "Market Analysis",
                "description": "Research competitors for the new product launch.",
                "date": "2025-02-04",
                "category": "Research"
            },
            {
                "active": false,
                "newTask": false,
                "completed": false,
                "failed": true,
                "title": "Onboarding Materials",
                "description": "Prepare onboarding materials for new hires.",
                "date": "2025-01-29",
                "category": "HR"
            }
        ],
        "taskStats": { "active": 1, "newTask": 1, "completed": 0, "failed": 1 }
    },
    {
        "id": 5,
        "firstName": "Karan",
        "email": "employee5@example.com",
        "password": "123",
        "tasks": [
            {
                "active": false,
                "newTask": true,
                "completed": false,
                "failed": false,
                "title": "Social Media Campaign",
                "description": "Plan and execute the February social media campaign.",
                "date": "2025-02-06",
                "category": "Marketing"
            },
            {
                "active": true,
                "newTask": false,
                "completed": false,
                "failed": false,
                "title": "Feedback Analysis",
                "description": "Analyze customer feedback from the latest survey.",
                "date": "2025-02-02",
                "category": "Customer Support"
            },
            {
                "active": false,
                "newTask": false,
                "completed": true,
                "failed": false,
                "title": "Code Review",
                "description": "Review the code changes submitted by the development team.",
                "date": "2025-01-26",
                "category": "Development"
            }
        ],
        "taskStats": { "active": 1, "newTask": 1, "completed": 1, "failed": 0 }
    }
];



export  const setLocalStorage = () =>{
    localStorage.setItem("employees",JSON.stringify(employees))
    localStorage.setItem("admin",JSON.stringify(admin))
}

export  const getLocalStorage = () =>{
    const employees = JSON.parse(localStorage.getItem("employees"))
    const admin = JSON.parse(localStorage.getItem("admin"))
   return {employees,admin}
}