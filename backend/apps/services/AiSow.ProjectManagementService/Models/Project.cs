using System;
using System.Collections.Generic;

namespace AiSow.ProjectManagementService.Models
{
    public class Project
    {
        public Guid Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public List<Document> Documents { get; set; } = new List<Document>();
    }
}
