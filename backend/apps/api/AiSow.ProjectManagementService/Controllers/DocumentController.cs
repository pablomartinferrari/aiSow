using Microsoft.AspNetCore.Mvc;
using AiSow.ProjectManagementService.Models;

namespace AiSow.ProjectManagementService.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class DocumentController : ControllerBase
    {
        // Placeholder for document endpoints
        // Implement as needed for your document model/repo
        [HttpGet]
        public IActionResult GetAll()
        {
            return Ok(new[] { new { Id = 1, Name = "Sample.pdf" } });
        }
    }
}
