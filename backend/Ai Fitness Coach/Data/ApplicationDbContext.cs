using Microsoft.EntityFrameworkCore;
using Ai_Fitness_Coach.Models;

namespace Ai_Fitness_Coach.Data
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options) { }

        public DbSet<User> Users { get; set; }
        public DbSet<WorkoutSession> WorkoutSessions { get; set; }
        public DbSet<WorkoutSet> WorkoutSets { get; set; }
        public DbSet<Exercise> Exercises { get; set; }
        public DbSet<ExerciseAnalysis> ExerciseAnalyses { get; set; }
        public DbSet<WorkoutAnalysis> WorkoutAnalyses { get; set; }
        public DbSet<ChatSession> ChatSessions { get; set; }
        public DbSet<ChatMessage> ChatMessages { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // --- User ---
            modelBuilder.Entity<User>()
                .HasIndex(u => u.Email)
                .IsUnique();

            modelBuilder.Entity<User>()
                .Property(u => u.Weight)
                .HasPrecision(18, 2);

            // --- WorkoutSession ---
            modelBuilder.Entity<WorkoutSession>()
                .HasOne(ws => ws.WorkoutAnalysis)
                .WithOne(wa => wa.WorkoutSession)
                .HasForeignKey<WorkoutAnalysis>(wa => wa.SessionId)
                .OnDelete(DeleteBehavior.Cascade);

            modelBuilder.Entity<WorkoutSession>()
                .HasMany(ws => ws.WorkoutSets)
                .WithOne(ws => ws.WorkoutSession)
                .HasForeignKey(ws => ws.WorkoutSessionId)
                .OnDelete(DeleteBehavior.Cascade);

            // --- WorkoutSet ---
            modelBuilder.Entity<WorkoutSet>()
                .Property(ws => ws.Weight)
                .HasPrecision(18, 2);

            // --- ExerciseAnalysis ---
            modelBuilder.Entity<ExerciseAnalysis>()
                .HasOne(ea => ea.WorkoutSession)
                .WithMany(ws => ws.ExerciseAnalyses)
                .HasForeignKey(ea => ea.WorkoutSessionId)
                .OnDelete(DeleteBehavior.NoAction);

            // --- ChatSession ---
            modelBuilder.Entity<ChatSession>()
                .HasMany(cs => cs.ChatMessages)
                .WithOne(cm => cm.ChatSession)
                .HasForeignKey(cm => cm.SessionId)
                .OnDelete(DeleteBehavior.Cascade);

            // --- Exercise ---
            modelBuilder.Entity<Exercise>()
                .HasQueryFilter(e => !e.IsDeleted);

            // --- Seed data ---
            modelBuilder.Entity<Exercise>().HasData(
                new Exercise { Id = 1, Name = "Squat", MuscleGroup = "Legs", Category = "Strength" },
                new Exercise { Id = 2, Name = "Bench Press", MuscleGroup = "Chest", Category = "Strength" },
                new Exercise { Id = 3, Name = "Deadlift", MuscleGroup = "Back", Category = "Strength" }
            );
        }
    }
}