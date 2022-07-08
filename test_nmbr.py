from nmbr import COUNT, CountWords, Nmbr, nmbr
import pytest


@pytest.mark.parametrize('n', (range(1, 7)))
def test_all_unsigned(n):
    N = Nmbr(n, signed=False)
    m = N.count(n)

    for i in range(m):
        words = N(i)
        assert len(words) == len(set(words))
        assert N(words) == i, str(words)

    err = 'Only accepts non-negative numbers'
    with pytest.raises(ValueError, match=err):
        N(-1)

    err = f'Cannot represent {m} in base {n}'
    with pytest.raises(ValueError, match=err):
        N(m)


@pytest.mark.parametrize('n', (range(1, 7)))
def test_all_signed(n):
    N = Nmbr(n)
    m = N.count(n)
    d = (m + 1) // 2
    r = range(d - m, d)

    for i in r:
        words = N(i)
        assert len(words) == len(set(words))
        assert N(words) == i, str(words)

    err = f'Cannot represent {r.start - 1} in base {n}'
    with pytest.raises(ValueError, match=err):
        N(r.start - 1)

    err = f'Cannot represent {r.stop} in base {n}'
    with pytest.raises(ValueError, match=err):
        N(r.stop)


def test_count():
    M = 2 ** 64 - 1

    def count(n, i):
        return CountWords(n)(i)

    assert count(COUNT, 6) > M > count(COUNT - 1, 6)
    assert count(COUNT, 6) > 1.0001 * M
    assert M / 1.003 > count(COUNT - 1, 6)


_STABILITY_TABLE = (
    (0, ['the']),
    (1, ['and']),
    (-1, ['of']),
    (-2, ['to']),
    (999, ['the', 'song']),
    (-32000, ['has', 'load']),
    (134123978423341234, ['as', 'ye', 'peak', 'hack', 'dies', 'songs']),
    (
        -341279384172341314120987134123443434734134913248132481234812341823413,
        [
            'new', 'taken', 'aged', 'hash', 'tier', 'aims', 'ash', 'dont',
            'liz', 'field', 'gold', 'told', 'palm', 'time', 'goat', 'set',
            'via', 'arc', 'ball', 'cute', 'arch', 'gang',
        ]
    ),
)


def test_stability():
    debug = not True
    if debug:
        print('_STABILITY_TABLE = (')

    for number, words in _STABILITY_TABLE:
        if debug:
            names = "', '".join(nmbr(number))
            print(f'    ({number}, [\'{names}\']),')
        else:
            assert nmbr(number) == words
            assert nmbr(words) == number

    if debug:
        print(')')

    assert not debug


def test_huge_signed():
    assert nmbr.count() == MAX
    assert nmbr.maxint == MAX // 2 - 1
    assert nmbr.minint == - MAX // 2

    expected = ['the', 'of', 'and', 'to', 'a', 'in', 'for', 'is']
    assert nmbr(nmbr.maxint)[:8] == expected

    expected = [
        'waste', 'chair', 'phase', 'motor', 'shirt', 'crime', 'claim', 'count'
    ]
    assert nmbr(nmbr.maxint)[-8:] == expected
    with pytest.raises(ValueError):
        nmbr(nmbr.maxint + 1)

    expected = ['the', 'of', 'and', 'to', 'a', 'in', 'for', 'is']
    assert nmbr(nmbr.minint)[:8] == expected

    expected = [
        'waste', 'chair', 'phase', 'motor', 'shirt', 'crime', 'count', 'claim'
    ]
    assert nmbr(nmbr.minint)[-8:] == expected
    with pytest.raises(ValueError):
        nmbr(nmbr.minint - 1)


def test_huge_unsigned():
    n = Nmbr(signed=False)

    assert n.count() == MAX
    assert n.maxint == MAX - 1
    assert n.minint == 0

    expected = ['the', 'of', 'and', 'to', 'a', 'in', 'for', 'is']
    assert n(n.maxint)[:8] == expected

    expected = [
        'waste', 'chair', 'phase', 'motor', 'shirt', 'crime', 'count', 'claim'
    ]
    assert n(n.maxint)[-8:] == expected
    with pytest.raises(ValueError):
        n(n.maxint + 1)

    expected = ['the']
    assert n(n.minint) == expected


MAX = int(
    '957593983838223553317964846178147830725566786818375245634851966468032086'
    '812095081023340149840027167874804807730838232628969642090838511734342843'
    '723031086571837144537191320088937374482203157694690563306553034785164378'
    '425384452102559333374028558941750785250754575004300724089603298331201725'
    '371146414107162790512623070617126391283941481740682076509694485498766328'
    '458574158082196735405704787217552634482812113237458096407369691067092884'
    '588113577740644732254101000362254827859045645705392429530637932542147188'
    '023435549378189206202277019096443766775401211622791231254109944674684567'
    '149020192723102644391777615157553803248978641573657072893923245924777719'
    '118946825671538779415255729222761250849713090026631879354758841213491877'
    '311274253800257570066847883464123212577649369124393539314368818877082467'
    '262243123114629278309622010128263241004030349895827068307484119953195281'
    '032633223232930534063186426416981938799619234104168443587642743041224955'
    '595988009201271620877341390258654057924205250736220852285881946429243766'
    '990370959052359290489441804281835896230018116628146689153484913763260562'
    '054912896987401349268837875102449173963084804357960236938450677039991381'
    '800826531022643100670253119818135031310163284115241404125275348776270552'
    '976156195160923811704537052861598544649042312184308389860891668764206754'
    '480005512325723120361837928150462190274662528992790406761270023335712989'
    '070582210128570893823177863092327475360945325922970808197159104082784527'
    '814654082969115334289770132828222816837799331081585521172246138890063320'
    '109173236138138116679620544903247562302062062643067208059114560748905562'
    '899978153917271328431245107203215105244056410930748390023725084105534565'
    '691330665303238355859963789180725010052010584467191175190056821063982086'
    '000301573510166811096025452078520191477732832175829792329523576916691043'
    '942492441604867475101348143705782036115444257875612846364098087412483879'
    '295887536375083349721243564559983722428601257960564750688418541296247278'
    '341879835795466385388591103057657412790727343365106597618192082474121804'
    '568000140051239832734635272903084073606962862226432448311784312923653722'
    '773123526589828107946653709112066559791335494445912883071823451933483194'
    '290741824153443016056067975084642385804116259197690019204839488812459650'
    '987569078992619487501595102795089646102383661564578209714691221726770705'
    '739638394817312175158848340323260917533233231354356732050139745868427510'
    '472562920968499140179137005009341129388189711881686618159729791438389032'
    '591208198639649825383582167556997771435518719516690074620428423188279511'
    '882628357145249931477346755338191571165347782311160471964008445921919178'
    '299543736531287040676880971782977791244468669504343297881427322032981776'
    '583011243348314540616156891628769693422456644115031814948719741617268702'
    '001890048523366341374786574673209041339228806514747160641585469787105617'
    '362123253485734110952014382243252595072891853408776931235768546570416498'
    '582995758789017872961431841965075580414656817488763974142808678198311709'
    '878877958714840422299381358787700798205049587037616780607411637808875111'
    '898326651391806854439205134331909463482441455273623280286293925349569743'
    '033055980646478670086240161775440285207880250306689428941411055892814560'
    '517794531574316092027652687431078912250605855668061785245263754640261447'
    '669131761907010975040287905092683057456958915960585591440197699772337709'
    '235296579574245481592144111917456346499972830493065222376012488207349126'
    '424868805483673549084839214042959562360249848490137631238185564049199250'
    '334454325917440080192332739726461886671588489506640314988355784447355937'
    '097047172744453717094975677904963900721030009073722262163618299965305228'
    '568396778063954011146204591235788629822630029010055181548706557048162034'
    '822559748475113403566338085737202104362605317152472029148845780880734133'
    '823486985089638391519406451617331393102525296246877533751630486305042536'
    '791651967186368880573214124805647057463352893849182224162229997764728471'
    '016616631815177757490936998494851412737666274393159807587105585507208182'
    '000917126623522185750603434025719439825908906020586461519972199729778860'
    '458159169990954735988720297233471336233471255064142386580127061237968294'
    '125305924368272320423999320445475307359361022458724805351130657411203984'
    '189312147865621228823904849438146404672532148685588474370768039307357266'
    '487648610376396480381111010702085870712925009813904761860050241839879954'
    '784301659099350525180999967617909143599850115718677794018738962981231410'
    '293495139804849316021784308890454297582993317757651454843834159036935423'
    '807423326149273600741451973889977658554269956526856096972640'
)
