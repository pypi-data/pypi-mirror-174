import triton
import triton.language as tl


@triton.jit
def lif_forward_kernel(
    output_spikes,
    vmem_all,
    input,
    vmem_post_initial,
    alpha,
    membr_subtract,
    theta,
    theta_low,
    apply_theta_low,
    max_num_spikes,
    num_neurons,
    num_timesteps,
):
    neuron_block_id = tl.program_id(0)
