using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using AiSow.ProjectManagementService.Models;
using AiSow.ProjectManagementService.Data;

namespace AiSow.ProjectManagementService.Repos
{
    public class ProjectRepository
    {
        private readonly AppDbContext _context;
        public ProjectRepository(AppDbContext context)
        {
            _context = context;
        }

        public async Task<List<Project>> GetAllAsync()
        {
            return await _context.Projects.Include(p => p.Documents).ToListAsync();
        }

        public async Task<Project?> GetByIdAsync(Guid id)
        {
            return await _context.Projects.Include(p => p.Documents).FirstOrDefaultAsync(p => p.Id == id);
        }

        public async Task<Project> AddAsync(Project project)
        {
            project.Id = Guid.NewGuid();
            _context.Projects.Add(project);
            await _context.SaveChangesAsync();
            return project;
        }

        public async Task<Project?> UpdateAsync(Project project)
        {
            var existing = await _context.Projects.FindAsync(project.Id);
            if (existing == null) return null;
            existing.Name = project.Name;
            existing.Description = project.Description;
            await _context.SaveChangesAsync();
            return existing;
        }

        public async Task<bool> RemoveAsync(Guid id)
        {
            var project = await _context.Projects.FindAsync(id);
            if (project == null) return false;
            _context.Projects.Remove(project);
            await _context.SaveChangesAsync();
            return true;
        }
    }
}
