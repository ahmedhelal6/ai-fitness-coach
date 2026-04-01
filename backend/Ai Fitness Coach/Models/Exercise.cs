using System.ComponentModel.DataAnnotations;

namespace Ai_Fitness_Coach.Models
{
    public class Exercise
    {
        [Key]
        public int Id { get; set; }
        [Required]
        [MaxLength(100)]
        public string Name { get; set; }=string.Empty;
        [Required]
        [MaxLength(100)]
        public string MuscleGroup { get; set; } = string.Empty;
        [Required]
        [MaxLength(100)]
        public string Category { get; set; } = string.Empty;
        public bool IsDeleted { get; set; } = false;

        public ICollection<WorkoutSet> WorkoutSets { get; set; } = new HashSet<WorkoutSet>();
        public ICollection<ExerciseAnalysis> ExerciseAnalyses { get; set; } = new HashSet<ExerciseAnalysis>();
    }
}
