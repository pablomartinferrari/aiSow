using Microsoft.EntityFrameworkCore;
using AiSow.ProjectManagementService.Models;

namespace AiSow.ProjectManagementService.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

        public DbSet<Project> Projects { get; set; }
        public DbSet<Document> Documents { get; set; }
    }
}
