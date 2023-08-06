# -*- coding:utf-8 -*-
from __future__ import division, unicode_literals

__author__ = 'denishuang'

import re
from xyz_util.datautils import strQ2B
from . import models, choices
from django.contrib.contenttypes.models import ContentType
from functools import reduce


def distrib_count(d, a, reverse=False):
    a = str(a)
    counts = d.setdefault('counts', {})
    percents = d.setdefault('percents', {})
    counts[a] = counts.setdefault(a, 0) + 1
    tc = sum(counts.values())
    cas = [(int(float(k)), v) for k, v in counts.items()]
    cas.sort(reverse=reverse)
    s = 0
    for k, v in cas:
        s += v
        percents[str(k)] = round(s / float(tc), 3)
    d['count'] = tc
    return d


def answer_is_empty(a):
    if isinstance(a, (list, tuple)):
        return not any(a)
    return not a


def answer_equal(standard_answer, user_answer):
    if len(standard_answer) != len(user_answer):
        return False
    l = zip(standard_answer, user_answer)
    return all([b in a.split('|') for a, b in l])


RE_MULTI_ANSWER_SPLITER = re.compile(r"[|()、]")


def split_answers(s):
    if isinstance(s, (list, tuple)):
        return s
    return RE_MULTI_ANSWER_SPLITER.split(strQ2B(s))


"""
In [36]: answer_match(['A|C','B','C','D'],['C','B'],True)
Out[36]: 0.5

In [37]: answer_match(['A','B','C','D'],['C','B'])
Out[37]: 0.5

In [38]: answer_match(['A','B','C','D'],['B'])
Out[38]: 0.25

In [39]: answer_match(['A','B','C','D'],['B'],True)
Out[39]: 0.0

In [40]: answer_match(['A','B','C','D'],['B','E'])
Out[40]: 0.0

In [41]: answer_match(['A','B','C','D'],['B','A','D','C'])
Out[41]: 1.0
"""


def answer_match(standard_answer, user_answer, one_by_one=False):
    sa = standard_answer
    ua = user_answer
    lsa = len(sa)
    lua = len(ua)
    if lua > lsa:
        return -1
    l = zip(sa[:lua], ua)
    c = 0
    for s, u in l:
        if one_by_one:
            if u in split_answers(s):
                c += 1
        else:
            if u in sa:
                c += 1
            else:
                c = 0
                break
    return c / lsa


def extract_fault(answer):
    m = dict([(a['number'], a) for a in answer.detail if not (answer_is_empty(a['userAnswer']) or a['right'])])
    p = answer.paper.content.data
    rs = []
    for g in p['groups']:
        for q in g['questions']:
            qnum = q['number']
            q['group'] = dict(title=g.get('title'), memo=g.get('memo'), number=g.get('number'))
            if qnum in m:
                rs.append((q, m[qnum]))
    return rs


def record_fault(answer):
    user = answer.user
    paper = answer.paper

    fs = extract_fault(answer)
    nums = [a['number'] for a in answer.detail]
    models.Fault.objects.filter(user=answer.user, paper=answer.paper).exclude(question_id__in=nums).update(
        is_active=False)
    for question, qanswer in fs:
        question_id = question['number']
        lookup = dict(user=user, paper=paper, question_id=question_id)
        fault = models.Fault.objects.filter(**lookup).first()
        if not fault:
            models.Fault.objects.create(
                question=question,
                question_type=choices.MAP_QUESTION_TYPE.get(question['type']),
                detail=dict(lastAnswer=qanswer), **lookup
            )
        else:
            fault.times += 1
            fault.detail['last_answer'] = qanswer
            fault.corrected = False
            fault.question = question
            fault.is_active = True
            fault.question_type = choices.MAP_QUESTION_TYPE.get(question['type'])
            from datetime import datetime
            fault.create_time = datetime.now()
            rl = fault.detail.setdefault('result_list', [])
            rl.append(False)
            fault.save()


def restruct_fault(paper):
    import textdistance
    jws = textdistance.JaroWinkler()

    qtm = {}
    from copy import deepcopy
    gs = deepcopy(paper.content.data.get('groups'))
    nums = []
    for g in gs:
        for q in g.get('questions'):
            q['group'] = dict(title=g.get('title'), memo=g.get('memo'), number=g.get('number'))
            qtm[q.get('title')] = q
            nums.append(q.get('number'))
    models.Fault.objects.filter(paper=paper).exclude(question_id__in=nums).update(is_active=False)
    bm = {True: [], False: []}
    for f in paper.faults.all():
        q = f.question
        t1 = q.get('title')
        tp1 = t1.split('题】')[-1]
        qn = None
        mdl = 0.8
        for t2 in qtm.keys():
            tp2 = t2.split('题】')[-1]
            dl = jws.similarity(tp1, tp2)
            if dl > mdl:
                qn = qtm.get(t2)
                mdl = dl
        if not qn:
            bm[False].append(f.id)
            f.is_active = False
            f.save()
            continue
        t2 = qn.get('title')
        if t1 != t2 \
                or q.get('options') != qn.get('options') \
                or q.get('answer') != qn.get('answer') \
                or q.get('explanation') != qn.get('explanation'):
            bm[True].append(f.id)
            f.question = qn
            f.save()
    return bm


def cal_correct_straight_times(rl):
    c = 0
    for i in range(len(rl) - 1, -1, -1):
        if not rl[i]:
            break
        c += 1
    return c


def check_token(request, pk):
    from django.core.signing import TimestampSigner
    import json, base64
    from datetime import datetime
    signer = TimestampSigner(salt=str(pk))
    qs = request.query_params
    token = qs.get('token')
    try:
        s = signer.unsign(token)
        s = base64.b64decode(s)
        d = json.loads(s)
        if d['exam'] != pk or d['expire'] <= datetime.now().isoformat():
            return {'detail': '验证码无效'}
    except:
        import traceback
        print(traceback.format_exc())
        return {'detail': '验证码无效'}


def chapter_name_normalize(n):
    r = re.compile(r'(\d+)')
    ps = r.split(n)
    if len(ps) != 3:
        return n
    i = int(ps[1])
    if i == 0:
        return '绪论'
    from xyz_util.datautils import digits2cn
    return ps[0] + digits2cn(i) + ps[2]


def group_name_sumary(n):
    r = re.compile(r'[(（,， .。:： <Ⅰ-Ⅹ]')
    return r.split(n)[0].strip()


def group_name_normalize(n):
    return choices.MAP_QUESTION_TYPE_NAME.get(n, n) + '题'


def gen_paper_from_other(title, cond, other, order_number=0):
    from .stores import QuestionStore
    from .models import Paper, Content
    st = QuestionStore()
    qts = st.gen_paper(cond)
    gs = []
    gc = 0
    qc = 0
    score = 0
    for qt, g in qts.items():
        gc += 1
        qs = g['questions']
        qc += len(qs)
        g.update(dict(title=qt, number=gc, questionCount=len(qs)))
        score += reduce(lambda a, b: a + b['score'], qs, 0)
        gs.append(g)
    cdata = dict(title=title, groups=gs, totalScore=score)
    paper, created = Paper.objects.update_or_create(
        user=other.user,
        owner_id=other.owner_id,
        owner_type=other.owner_type,
        title=title,
        tags='章节习题',
        defaults=dict(
            is_active=True,
            order_number=order_number,
            questions_count=qc
        ))
    content, created = Content.objects.update_or_create(
        paper=paper,
        defaults=dict(
            data=cdata
        )
    )
    return paper


def backup_old_chaper_papers(owner):
    ct = ContentType.objects.get_for_model(owner)
    old = '章节习题'
    new = '章节习题（备份）'
    c = models.Paper.objects.filter(
        owner_id=owner.pk,
        owner_type=ct,
        tags=new,
        is_active=False
    ).count()
    if c > 0:
        return
    print('备份%s试卷:%s' % (old, owner))
    models.Paper.objects.filter(
        owner_id=owner.pk,
        owner_type=ct,
        tags=old
    ).update(
        tags=new,
        is_active=False
    )


def gen_chapter_papers(owner):
    ct = ContentType.objects.get_for_model(owner)
    other = models.Paper.objects.filter(owner_id=owner.pk, owner_type=ct).first()
    tname = owner._meta.label_lower
    ps = []
    no = 0
    SUB_LIST = [v for k, v in choices.MAP_QUESTION_TYPE_NO.items() if k in choices.SUBJECTIVE_TYPES]
    OBJ_LIST = [v for k, v in choices.MAP_QUESTION_TYPE_NO.items() if k not in choices.SUBJECTIVE_TYPES]
    categories = [('客观题', OBJ_LIST), ('主观题', SUB_LIST)]
    for n in owner:
        ols = [sn.name for sn in n.items]
        for cn, cts in categories:
            pname = '%s %s（%s）' % (chapter_name_normalize(n.prefix), n.name, cn)
            cond = {
                'ownerType': tname,
                'ownerId': owner.pk,
                'type': {'$in': cts},
                'outline': {'$in': ols}
            }
            paper = gen_paper_from_other(pname, cond, other, order_number=no)
            ps.append(paper)
            no += 1
    return ps
