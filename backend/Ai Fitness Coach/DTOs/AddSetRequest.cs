namespace Ai_Fitness_Coach.DTOs
{
    public class AddSetRequest
    {
        public int WorkoutSessionId { get; set; }
        public int ExerciseId { get; set; }
        public int Reps { get; set; }
        public decimal? Weight { get; set; }
    }
}
