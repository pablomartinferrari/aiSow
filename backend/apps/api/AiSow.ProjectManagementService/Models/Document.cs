using System;

namespace AiSow.ProjectManagementService.Models
{
    public class Document
    {
        public Guid Id { get; set; }
        public string FileName { get; set; } = string.Empty;
        public Guid ProjectId { get; set; }
        public Project? Project { get; set; }
    }
}
