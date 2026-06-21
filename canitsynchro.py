import sys
import argparse

def calculate_step_up(ratio_current, ratio_harder):
    return (ratio_harder / ratio_current) - 1.0

def calculate_step_down(ratio_current, ratio_easier):
    return 1.0 - (ratio_easier / ratio_current)

def main():
    parser = argparse.ArgumentParser(
        description="Constraint based crossover calculator for shimano synchro shift",
        usage='python3 canitsynchro.py "[cassette]" "[chainrings]" [options]',
        epilog="""
Examples:
  # calculation with 2x11 MTB using default constraints
  python3 canitsynchro.py "11,13,15,17,19,21,24,27,31,35,40" "26/36"

  # Gravel 2x12 Setup with looser constraints
  python3 canitsynchro.py "11,12,13,14,15,17,19,21,24,30,34" "30/46" -min 0.05 -max 0.16 -adj 0.1 -small 1 -big 0
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('cassette', type=str, help='Comma or space separated string of cogs')
    parser.add_argument('chainrings', type=str, help='Slash separated string of small/large chainrings')

    parser.add_argument('-min', type=float, default=0.08, help='Minimum Jump in percent divided by 100 (default: 0.08)')
    parser.add_argument('-max', type=float, default=0.16, help='Maximum Jump in percent divided by 100 (default: 0.16)')
    parser.add_argument('-adj', type=float, default=0.1, help='Adjacent shift tolerance, i.e compare percentual jump to the ones that come before/after (default: 0.1)')

    parser.add_argument('-small', type=int, default=3, help='Number of small cogs to restrict on the small ring (default: 3)')
    parser.add_argument('-big', type=int, default=2, help='Number of large cogs to restrict on the big ring (default: 2)')

    args = parser.parse_args()

    try:
        cassette = sorted(list(set([int(c.strip()) for c in args.cassette.replace(',', ' ').split() if c.strip()])))
        chainrings = sorted([int(r.strip()) for r in args.chainrings.split('/') if r.strip()])
        if len(chainrings) != 2:
            raise ValueError("W: Chainrings must look like: '34/50'")
        cr_small, cr_large = chainrings[0], chainrings[1]
    except Exception as e:
        print(f"E: Input Parsing Error: {e}", file=sys.stderr)
        sys.exit(1)

    # cross-chain
    min_small_ring_cog = cassette[args.small] if args.small > 0 else cassette[0]
    max_big_ring_cog = cassette[-args.big - 1] if args.big > 0 else cassette[-1]

    print(f"--- Drivetrain Configuration ---")
    print(f"Cassette:            {cassette}")
    print(f"Chainrings:          {cr_small}T / {cr_large}T")
    print(f"Jump Constraints:         Min Jump: {args.min*100:.1f}%, Max Jump: {args.max*100:.1f}%, Adj Tol: ±{args.adj*100:.1f}%")
    print(f"Crosschain restrictions:       Small ring cogs < {min_small_ring_cog}T  (first {args.small})")
    print(f"                               Large ring cogs > {max_big_ring_cog}T (last {args.big})\n")

    valid_upshifts = []
    valid_downshifts = []

    # calculate upshifts
    for i in range(1, len(cassette)):
        cog_small_trigger = cassette[i]
        if cog_small_trigger < min_small_ring_cog:
            continue
        cog_small_adj_harder = cassette[i - 1]

        ratio_current = cr_small / cog_small_trigger
        ratio_adj_harder = cr_small / cog_small_adj_harder
        adj_rear_jump = calculate_step_up(ratio_current, ratio_adj_harder)

        for j in range(len(cassette)):
            cog_big_target = cassette[j]
            if cog_big_target > max_big_ring_cog:
                continue
            ratio_big_target = cr_large / cog_big_target

            if ratio_big_target > ratio_current:
                jump = calculate_step_up(ratio_current, ratio_big_target)
                if args.min <= jump <= args.max:
                    if abs(jump - adj_rear_jump) <= args.adj:
                        valid_upshifts.append({
                            'trigger_cog': cog_small_trigger,
                            'target_cog': cog_big_target,
                            'target_idx': j,
                            'jump': jump,
                            'adj_jump': adj_rear_jump
                        })

    # calculate downshifts
    for j in range(len(cassette) - 1):
        cog_big_trigger = cassette[j]
        if cog_big_trigger > max_big_ring_cog:
            continue
        cog_big_adj_easier = cassette[j + 1]

        ratio_current = cr_large / cog_big_trigger
        ratio_adj_easier = cr_large / cog_big_adj_easier
        adj_rear_jump = calculate_step_down(ratio_current, ratio_adj_easier)

        for i in range(len(cassette)):
            cog_small_target = cassette[i]
            if cog_small_target < min_small_ring_cog:
                continue
            ratio_small_target = cr_small / cog_small_target

            if ratio_small_target < ratio_current:
                jump = calculate_step_down(ratio_current, ratio_small_target)
                if args.min <= jump <= args.max:
                    if abs(jump - adj_rear_jump) <= args.adj:
                        valid_downshifts.append({
                            'trigger_cog': cog_big_trigger,
                            'trigger_idx': j,
                            'target_cog': cog_small_target,
                            'jump': jump,
                            'adj_jump': adj_rear_jump
                        })

    # check calculation
    matched_pairs = []
    for up in valid_upshifts:
        for down in valid_downshifts:
            actual_hysteresis = down['trigger_idx'] - up['target_idx']
            # fix the logic edge cases
            if actual_hysteresis >= 0:
                matched_pairs.append((actual_hysteresis, up, down))

    matched_pairs.sort(key=lambda x: x[0])

    # display result
    if matched_pairs:
        print(f"\n > This drivetrain can synchro shift with {len(matched_pairs)} Match(es):")
        for separation, up, down in matched_pairs:
            print(f"    UPSHIFT:   At {cr_small}x{up['trigger_cog']}T -> Shift to {cr_large}x{up['target_cog']}T (Jump Percentage: {up['jump']*100:.2f}%)")
            print(f"    DOWNSHIFT: At {cr_large}x{down['trigger_cog']}T -> Shift to {cr_small}x{down['target_cog']}T (Jump Percentage: {down['jump']*100:.2f}%)")
            print(f"  Hysteresis: {separation} Gear(s)")
            print(f"    ----------------------------------------------------------------")
    else:
        print("\nE: This drivetrain can't synchro shift under these constraints. Try loosening parameters or checking for Input mistakes")

if __name__ == "__main__":
    main()
