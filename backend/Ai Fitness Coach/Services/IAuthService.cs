using Ai_Fitness_Coach.DTOs;

namespace Ai_Fitness_Coach.Services
{
    public interface IAuthService
    {
        Task<AuthResponse> RegisterAsync(RegisterRequest request);
        Task<AuthResponse> LoginAsync(LoginRequest request);
    }
}
