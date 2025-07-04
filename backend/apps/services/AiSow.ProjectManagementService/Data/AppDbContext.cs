using Microsoft.EntityFrameworkCore;
using AiSow.ProjectManagementService.Models;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;

namespace AiSow.ProjectManagementService.Data
{
    public class AppDbContext : IdentityDbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

        public DbSet<Project> Projects { get; set; }
        public DbSet<Document> Documents { get; set; }
    }
}
