using Microsoft.AspNetCore.Mvc;
using AiSow.ProjectManagementService.Models;
using AiSow.ProjectManagementService.Repos;

namespace AiSow.ProjectManagementService.Controllers
{
    [ApiController]
    [Route("api/projects")]
    public class ProjectController : ControllerBase
    {
        private readonly ProjectRepository _repo;

        public ProjectController(ProjectRepository repo)
        {
            _repo = repo;
        }

        [HttpGet]
        public async Task<IActionResult> GetAll()
        {
            var projects = await _repo.GetAllAsync();
            return Ok(projects);
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> GetById(Guid id)
        {
            var project = await _repo.GetByIdAsync(id);
            if (project == null) return NotFound();
            return Ok(project);
        }

        [HttpPost]
        public async Task<IActionResult> Create(Project project)
        {
            var created = await _repo.AddAsync(project);
            return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> Update(Guid id, Project project)
        {
            project.Id = id;
            var updated = await _repo.UpdateAsync(project);
            if (updated == null) return NotFound();
            return Ok(updated);
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> Delete(Guid id)
        {
            var deleted = await _repo.RemoveAsync(id);
            if (!deleted) return NotFound();
            return NoContent();
        }
    }
}
